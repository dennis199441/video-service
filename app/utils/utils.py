import cv2
import os

INPUT_DIR = "/usr/src/app/input"
OUTPUT_DIR = "/usr/src/app/output"


def getVideos():
    return filter(lambda x: x.lower().endswith("mp4") or x.lower().endswith("mov"), os.listdir(INPUT_DIR))


def getVideoWriter(filename, width, height):
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    return cv2.VideoWriter(f"{OUTPUT_DIR}/{filename}", fourcc, 29.98, (width, height))


def outputMP4Video(filename, width, height, frames):
    writer = getVideoWriter(filename, width, height)
    for frame in frames:
        writer.write(frame)
    writer.release()
