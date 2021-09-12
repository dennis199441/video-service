import cv2
import os
import time
from app.utils.utils import outputMP4Video


INPUT_DIR = "/usr/src/app/input"

def getTimelapseFrame(vid):
    frames = []
    success, count, speed = 1, 0, 8
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    while success:
        success, frame = vid.read()
        if count % speed == 0:
            frames.append(frame)
        count += 1
    return frames, width, height


def run_timelapse(filename):
    vid = cv2.VideoCapture(f"{INPUT_DIR}/{filename}")
    frames, width, height = getTimelapseFrame(vid)
    out_name = filename.lower().replace("mov", "mp4")
    outputMP4Video(out_name, width, height, frames)
