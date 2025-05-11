#!/bin/bash

tmux new-session -d -s yolov5

tmux send-keys -t yolov5 'cd ../yolov5' ENTER

tmux send-keys -t yolov5 'conda activate yolo' ENTER

tmux send-keys -t yolov5 "python train.py --data ../labeling/mydata.yaml --epochs 1000 --weights ' ' --cfg yolov5n.yaml --batch-size 64" ENTER