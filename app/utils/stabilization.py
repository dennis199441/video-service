import numpy as np
import cv2
import os
import time
from app.utils.utils import outputMP4Video

INPUT_DIR = "/usr/src/app/input"

SMOOTHING_RADIUS = 30


def estimateMotion(vid):
    n_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

    _, prev = vid.read()
    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    transforms = np.zeros((n_frames - 1, 3), np.float32)

    for i in range(n_frames - 2):
        # detect feature points in previous frame
        prev_pts = cv2.goodFeaturesToTrack(
            prev_gray, maxCorners=200, qualityLevel=0.01, minDistance=30, blockSize=3)

        success, cur = vid.read()
        if not success:
            break

        cur_gray = cv2.cvtColor(cur, cv2.COLOR_BGR2GRAY)

        # calculate optical flow
        cur_pts, status, err = cv2.calcOpticalFlowPyrLK(
            prev_gray, cur_gray, prev_pts, None)

        assert prev_pts.shape == cur_pts.shape

        # Filter only valid points
        idx = np.where(status == 1)[0]
        prev_pts = prev_pts[idx]
        cur_pts = cur_pts[idx]

        # transformation matrix
        m, _ = cv2.estimateAffinePartial2D(prev_pts, cur_pts)
        # translation
        dx, dy = m[0, 2], m[1, 2]
        # rotation
        da = np.arctan2(m[1, 0], m[0, 0])

        transforms[i] = [dx, dy, da]
        prev_gray = cur_gray

    return transforms, width, height


def movingAverage(curve, radius):
    window_size = 2 * radius + 1
    f = np.ones(window_size) / window_size
    curve_pad = np.lib.pad(curve, (radius, radius), "edge")
    curve_smoothed = np.convolve(curve_pad, f, mode="same")
    curve_smoothed = curve_smoothed[radius:-radius]
    return curve_smoothed


def smooth(trajectory):
    smoothed_trajectory = np.copy(trajectory)
    for i in range(3):
        smoothed_trajectory[:, i] = movingAverage(
            trajectory[:, i], radius=SMOOTHING_RADIUS)
    return smoothed_trajectory


def calculateSmoothTransforms(smoothed_trajectory, trajectory, transforms):
    difference = smoothed_trajectory - trajectory
    transforms_smooth = transforms + difference
    return transforms_smooth


def calculateSmoothMotion(transforms):
    trajectory = np.cumsum(transforms, axis=0)
    smoothed_trajectory = smooth(trajectory)
    transforms_smooth = calculateSmoothTransforms(
        smoothed_trajectory, trajectory, transforms)
    return transforms_smooth


def fixBorder(frame):
    s = frame.shape
    T = cv2.getRotationMatrix2D((s[1]/2, s[0]/2), 0, 1.04)
    frame = cv2.warpAffine(frame, T, (s[1], s[0]))
    return frame


def applySmoothedMotion(vid, transforms_smooth):
    n_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    finalized_frames = []
    vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
    for i in range(n_frames - 2):
        success, frame = vid.read()
        if not success:
            break

        dx = transforms_smooth[i, 0]
        dy = transforms_smooth[i, 1]
        da = transforms_smooth[i, 2]

        m = np.zeros((2, 3), np.float32)
        m[0, 0] = np.cos(da)
        m[0, 1] = -np.sin(da)
        m[1, 0] = np.sin(da)
        m[1, 1] = np.cos(da)
        m[0, 2] = dx
        m[1, 2] = dy

        frame_stabilized = cv2.warpAffine(frame, m, (width, height))
        frame_stabilized = fixBorder(frame_stabilized)
        frame_out = cv2.hconcat([frame, frame_stabilized])

        if frame_out.shape[1] > 1920:
            frame_out = cv2.resize(
                frame_out, (frame_out.shape[1] // 2, frame_out.shape[0] // 2))

        # cv2.imshow("Before and After", frame_out)
        # cv2.waitKey(10)
        finalized_frames.append(frame_stabilized)

    return finalized_frames


def run_stabilization(filename):
    vid = cv2.VideoCapture(f"{INPUT_DIR}/{filename}")
    transforms, width, height = estimateMotion(vid)
    transforms_smooth = calculateSmoothMotion(transforms)
    finalized_frames = applySmoothedMotion(vid, transforms_smooth)
    out_name = filename.lower().replace("mov", "mp4")
    outputMP4Video(out_name, width, height, finalized_frames)