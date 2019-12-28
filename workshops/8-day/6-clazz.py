#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
    视频的读写与处理
        FPS即每秒多少帧的处理能力，一般情况下（人类对300毫秒以下的变动是无法察觉的）每秒大于5帧的处理可以认为是视屏处理
"""


def process(frame, option):
    dst = frame
    if 1 == option:
        dst = cv.bitwise_not(frame)
    if 2 == option:
        dst = cv.GaussianBlur(frame, (0, 0), 15)
    if 3 == option:
        dst = cv.Canny(frame, 100, 200)
    return dst


def main():
    capture = cv.VideoCapture(0)
    # 获取视屏的fps
    fps = np.int32(capture.get(cv.CAP_PROP_FPS))
    option = 0
    while True:
        ret, frame = capture.read()
        if True is not ret:
            print("can't read video")
            break
        key = cv.waitKey(fps)
        if key >= 49:
            option = key - 48
        result = process(frame, option)
        cv.imshow("result", result)
        # ESC
        if 27 == key:
            break
    capture.release()
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
