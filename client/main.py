# encoding: utf-8
import asyncio
import base64
import uuid
import cv2
import json
import logging
import websockets
from auth_util import gen_sign_headers
from collections import Counter, deque
import aiohttp

# 配置统一的日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('combined.log', encoding='utf-8'),  # 指定文件编码为 UTF-8
        logging.StreamHandler()
    ]
)
# 请替换APP_ID、APP_KEY
APP_ID = '2025450647'
APP_KEY = 'ZRSQrcUjznHJeQnj'
URI = '/vivogpt/completions/stream'
DOMAIN = 'api-ai.vivo.com.cn'
METHOD = 'POST'

# WebSocket 服务器地址
cloud_uri = ["ws://202.114.212.195:50511/detect", "ws://202.114.212.193:50511/detect"]
front_video_uri = ["ws://localhost:7979?client_id=client1"]
front_status_uri = "ws://localhost:6868?client_id=client1"
window_size = 30
step = 10

# 独立的队列管理器，确保 AI 处理最新的帧
class LatestFrameQueue:
    def __init__(self):
        self.latest_frame = None
        self.lock = asyncio.Lock()

    async def put(self, frame):
        async with self.lock:
            self.latest_frame = frame

    async def get(self):
        async with self.lock:
            return self.latest_frame

def save_image(buffer, filename):
    with open(filename, "wb") as f:
        f.write(buffer)

async def stream_vivogpt(ai_queue, yolo_status_deque):
    while True:
        # 获取最新的帧
        latest_image = await ai_queue.get()
        if latest_image is None:
            break

        # 调用 AI 服务
        params = {
            'requestId': str(uuid.uuid4())
        }
        image_data = base64.b64encode(latest_image).decode('utf-8')
        data = {
            'prompt': '你好',
            'sessionId': str(uuid.uuid4()),
            'requestId': params['requestId'],
            'model': 'BlueLM-Vision-prd',
            "messages": [
                {
                    "role": "user",
                    "content": "data:image/JPEG;base64," + image_data,
                    "contentType": "image"
                },
                {
                    "role": "user",
                    "content": "用最简短的语言回答三个问题：嘴巴是张开的还是闭上的？脸正对着摄像头吗？眼睛睁开还是闭上？",
                    "contentType": "text"
                }
            ],
        }
        headers = gen_sign_headers(APP_ID, APP_KEY, METHOD, URI, params)
        headers['Content-Type'] = 'application/json'

        url = f'http://{DOMAIN}{URI}'
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers, params=params) as response:
                if response.status == 200:
                    response_text = ""
                    async for line in response.content:
                        line_text = line.decode('utf-8', errors='ignore').strip()
                        if "DONE" in line_text:
                            continue
                        if line_text.strip().startswith("data:"):
                            json_data = line_text.strip().replace("data:", "").strip()
                            data = json.loads(json_data)
                            if 'message' in data:
                                response_text += data['message']
                    if response_text.strip() != "。":
                        # 解析 AI 的回答并判断状态
                        state = determine_state(response_text)
                        logging.info(f"AI response {response_text}")
                        logging.info(f"State: {state}")
                        # 比较 AI 状态和 YOLO 状态
                        if state not in yolo_status_deque:
                            logging.warning(f"AI state {state} does not match any of the recent 10 YOLO states")
                else:
                    logging.error(f"AI response error: {response.status}")

def determine_state(response_text):
    """
    根据 AI 的回答解析状态
    """
    if "没有正对" in response_text or "侧对" in response_text:
        return 3
    elif "嘴巴是张开" in response_text or "嘴巴张开" in response_text:
        return 2
    elif "眼睛是闭上" in response_text or "眼睛闭上" in response_text or "眼睛闭着" in response_text or "眼睛也是闭上" in response_text:
        return 1
    else:
        return 0  # 默认状态

async def capture_camera(frame_queue, ai_queue):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logging.error("Failed to open camera")
        return

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                logging.warning("Failed to read frame")
                break

            _, buffer = cv2.imencode('.jpg', frame)
            img_str = base64.b64encode(buffer)
            save_image(buffer, "test.jpg")
            await frame_queue.put(img_str)  # 将帧放入 YOLO 队列
            await ai_queue.put(buffer.tobytes())  # 将帧放入 AI 队列
            await asyncio.sleep(0.01)
    finally:
        cap.release()
        logging.info("Video capture finished")
        await frame_queue.put(None)  # 放入 None 表示队列结束
        await ai_queue.put(None)

async def video_websocket(URI_list, queue, send_queue=None, yolo_status_deque=None):
    URI = URI_list[0]
    curURI = 0
    key = "cloud" if URI == cloud_uri[0] else "front"
    window = []
    while True:
        try:
            async with websockets.connect(URI) as websocket:
                logging.info(f"Successfully connected to {key}")
                while True:
                    img_str = await queue.get()
                    if img_str is None:
                        break
                    await websocket.send(img_str)
                    if URI in cloud_uri:
                        response = await websocket.recv()
                        if isinstance(response, str):
                            result = json.loads(response)
                            window.append(result['detected_class'])
                            logging.info(f"Received result from cloud: {result['detected_class']}")
                            # 将 YOLO 状态添加到 deque 中
                            if yolo_status_deque is not None:
                                yolo_status_deque.append(result['detected_class'])
                                if len(yolo_status_deque) > 10:
                                    yolo_status_deque.popleft()
                        if len(window) == window_size:
                            counter = Counter(window)
                            most_common, _ = counter.most_common(1)[0]
                            await send_queue.put(most_common)
                            window = window[step:]
        except websockets.ConnectionClosed:
            logging.error(f"Connection to {key} closed")
        except Exception as e:
            logging.error(f"Failed to connect to {key}: {e}")

        if len(URI_list) > 1:
            curURI = (curURI + 1) % len(URI_list)
            URI = URI_list[curURI]
            logging.info(f"Switching to {URI}")
        await asyncio.sleep(0.1)

async def status_websocket(URI, queue):
    key = "status"
    try:
        async with websockets.connect(URI) as websocket:
            while True:
                status = await queue.get()
                if status is None:
                    break
                await websocket.send(str(status))
    except Exception as e:
        logging.error(f"Failed to connect to {key}: {e}")

async def main():
    frame_queue = asyncio.Queue(maxsize=100)  # 增大队列大小
    ai_queue = LatestFrameQueue()  # 使用独立的队列管理器
    status_queue = asyncio.Queue(maxsize=10)
    yolo_status_deque = deque(maxlen=10)  # 存储最近 10 个 YOLO 状态
    await asyncio.gather(
        capture_camera(frame_queue, ai_queue),
        video_websocket(cloud_uri, frame_queue, status_queue, yolo_status_deque),
        video_websocket(front_video_uri, frame_queue),
        status_websocket(front_status_uri, status_queue),
        stream_vivogpt(ai_queue, yolo_status_deque)  # 异步调用 AI 服务
    )

if __name__ == "__main__":
    asyncio.run(main())