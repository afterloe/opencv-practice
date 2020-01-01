#!/usr/bin/env python3
# -*- coding=utf-8 -*-


import cv2 as cv
from goto import with_goto
import numpy as np


"""
    稠密光流分析
        光流分析分稀疏与稠密两种，在opencv 4.0后Opencv支持两种稠密光流计算方法
    相关api如下:

    cv.calcOpticalFlowFarneback()

"""


@with_goto
def main():
    capture = cv.VideoCapture("../../../raspberry-auto/pic/vtest.avi")
    ret, frame = capture.read()
    if True is not ret:
        print("can't read video!")
        goto .end
    prv_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame)
    hsv[..., 1] = 255
    while True:
        ret, frame = capture.read()
        if True is not ret:
            print("video is end!")
            break
        next_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        flow = cv.calcOpticalFlowFarneback(prv_frame, next_frame, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])
        hsv[..., 0] = ang * 180 / np.pi / 2
        hsv[..., 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
        bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
        cv.imshow("frame", bgr)
        key = cv.waikKey(1) & 0xff
        if 27 == key:
            break
        prv_frame = next_frame

    label .end
    capture.release()
    cv.destoryAllWindows()



if "__main__" == __name__:
    main()

