import gevent
from gevent import monkey
monkey.patch_all()
import struct
import json
import sys
import time
from websocket import create_connection
from auth_util import gen_sign_headers
import pyaudio  # 用于捕获麦克风音频
import requests
import wave
import io
import uuid
from urllib import parse


# 音频参数
NUM = 1
CHUNK = 1024  # 每次捕获的音频数据块大小
FORMAT = pyaudio.paInt16  # 音频格式
CHANNELS = 1  # 单声道
RATE = 16000  # 采样率
RECORD_SECONDS = 5  # 录音时长（可以根据需要调整）

# 云端 AI 的 APP_ID 和 APP_KEY
APP_ID = '2025450647'
APP_KEY = 'ZRSQrcUjznHJeQnj'
DOMAIN = 'api-ai.vivo.com.cn'

def read_microphone_data(stream):
    """
    从麦克风捕获音频数据
    """
    data = stream.read(CHUNK)
    return data

def send_process(ws, stream):
    try:
        start_data = {
            "type": "started",
            "request_id": "req_id",
            "asr_info": {
                "front_vad_time": 6000,
                "end_vad_time": 2000,
                "audio_type": "pcm",
                "chinese2digital": 1,
                "punctuation": 2,
            },
            "business_info": "{\"scenes_pkg\":\"com.tencent.qqlive\", \"editor_type\":\"3\", \"pro_id\":\"2addc42b7ae689dfdf1c63e220df52a2-2020\"}"
        }

        start_data_json_str = json.dumps(start_data)
        ws.send(start_data_json_str)

        silence_threshold = 1000  # 静音阈值
        silence_duration = 3.0  # 静音时长（秒）
        silence_frames = int(silence_duration * RATE / CHUNK)
        consecutive_silence = 0  # 连续静音帧数

        while True:
            wav_data = read_microphone_data(stream)
            if max(wav_data) < silence_threshold:
                consecutive_silence += 1
                if consecutive_silence >= silence_frames:
                    break  # 检测到足够长的静音，结束录音
            else:
                consecutive_silence = 0  # 重置静音计数

            ws.send_binary(wav_data)
            time.sleep(0.04)

        enddata = b'--end--'
        ws.send_binary(enddata)

        closedata = b'--close--'
        ws.send_binary(closedata)
    except Exception as e:
        print(f"发送过程中发生错误: {e}")
        return

def recv_process(ws, tbegin):
    while True:
        try:
            r = ws.recv()
            tmpobj = json.loads(r)

            if tmpobj["action"] == "result" and tmpobj["type"] == "asr" and tmpobj["data"]["is_last"]:
                recognized_text = tmpobj["data"]["text"]
                print(f"您说的内容: {recognized_text}")  # 打印用户说的话
                return recognized_text  # 返回识别的文本

        except Exception as e:
            print(f"接收过程中发生错误: {e}")
            return None

def control_process():
    t = int(round(time.time() * 1000))

    params = {'client_version': parse.quote('unknown'), 'product': parse.quote('x'), 'package': parse.quote('unknown'),
              'sdk_version': parse.quote('unknown'), 'user_id': parse.quote('2addc42b7ae689dfdf1c63e220df52a2'),
              'android_version': parse.quote('unknown'), 'system_time': parse.quote(str(t)), 'net_type': 1,
              'engineid': "shortasrinput"}

    uri = '/asr/v2'
    headers = gen_sign_headers(APP_ID, APP_KEY, 'GET', uri, params)

    param_str = ''
    seq = ''

    for key, value in params.items():
        value = str(value)
        param_str = param_str + seq + key + '=' + value
        seq = '&'

    # 初始化 PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    ws = create_connection('ws://' + DOMAIN + '/asr/v2?' + param_str, header=headers)
    co1 = gevent.spawn(send_process, ws, stream)
    recognized_text = gevent.spawn(recv_process, ws, t).get()  # 获取识别的文本
    gevent.joinall([co1])

    # 关闭麦克风流
    stream.stop_stream()
    stream.close()
    p.terminate()

    return recognized_text  # 返回识别的文本

def get_ai_response(text):
    URI = '/vivogpt/completions'
    METHOD = 'POST'

    params = {
        'requestId': str(uuid.uuid4())
    }

    data = {
        'prompt': text,
        'model': 'vivo-BlueLM-TB-Pro',
        'sessionId': str(uuid.uuid4()),
        'extra': {
            'temperature': 0.9
        }
    }
    headers = gen_sign_headers(APP_ID, APP_KEY, METHOD, URI, params)
    headers['Content-Type'] = 'application/json'

    url = 'https://' + DOMAIN + URI
    response = requests.post(url, json=data, headers=headers, params=params)

    if response.status_code == 200:
        res_obj = response.json()
        if res_obj['code'] == 0 and res_obj.get('data'):
            ai_response = res_obj['data']['content']
            print(f"AI的回答: {ai_response}")  # 打印 AI 的回答
            return ai_response
    else:
        print(f"请求 AI 服务失败，状态码: {response.status_code}, 响应内容: {response.text}")
    return None

def pcm2wav(pcmdata: bytes, channels=1, bits=16, sample_rate=24000):
    if bits % 8 != 0:
        raise ValueError("bits % 8 must == 0. now bits:" + str(bits))
    io_fd = io.BytesIO()
    wavfile = wave.open(io_fd, 'wb')
    wavfile.setnchannels(channels)
    wavfile.setsampwidth(bits // 8)
    wavfile.setframerate(sample_rate)
    wavfile.writeframes(pcmdata)
    wavfile.close()
    io_fd.seek(0)
    return io_fd

def play_wav(wav_io):
    CHUNK = 1024
    p = pyaudio.PyAudio()
    wf = wave.open(wav_io, 'rb')
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()

def text_to_speech(text):
    from tts_examples import TTS, AueType

    input_params = {
        'app_id': APP_ID,
        'app_key': APP_KEY,
        'engineid': 'short_audio_synthesis_jovi'
    }
    tts = TTS(**input_params)
    tts.open()

    #修改vcn以切换音色
    pcm_buffer = tts.gen_radio(aue=AueType.PCM, vcn="yiyi", text=text)
    wav_io = pcm2wav(pcm_buffer)
    play_wav(wav_io)

def main():
    while True:  # 无限循环
        print("呼叫小明同学以开始对话...")
        recognized_text = control_process()  # 获取识别的文本
        if recognized_text:
            if "小明" in recognized_text:
                recognized_text = '你是一个叫小明车载语音助手，用二十字以内的的语言回答：' + recognized_text
                ai_response = get_ai_response(recognized_text)
                if ai_response :
                    text_to_speech(ai_response)  # 将 AI 的回答转换为语音并播放
                else :
                    print("AI未正常回答")
            else:
                print("请先说出小明同学")
        else:
            print("未识别到有效文本")

if __name__ == "__main__":
    main()