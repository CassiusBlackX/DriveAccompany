import os
import cv2
import random

def extract_frames_from_videos(input_path, output_path, frames_per_second=3):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for root, _, files in os.walk(input_path):
        for file in files:
            if file.endswith(('.mp4', '.avi', '.mov', '.mkv')):
                video_path = os.path.join(root, file)
                capture = cv2.VideoCapture(video_path)
                fps = int(capture.get(cv2.CAP_PROP_FPS))
                total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
                duration = total_frames // fps

                for second in range(duration):
                    frame_indices = random.sample(range(second * fps, (second + 1) * fps), frames_per_second)
                    for frame_index in frame_indices:
                        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
                        ret, frame = capture.read()
                        if ret:
                            frame_filename = f"{os.path.splitext(file)[0]}_frame_{frame_index}.jpg"
                            frame_filepath = os.path.join(output_path, frame_filename)
                            cv2.imwrite(frame_filepath, frame)
                        else:
                            print(f"Failed to read frame at index {frame_index} from {video_path}")

                capture.release()

if __name__ == "__main__":
    input_path = r"E:\AO\se\videos"
    output_path = r"E:\AO\se\software-engineering-516\backend\labeling\images"
    extract_frames_from_videos(input_path, output_path)