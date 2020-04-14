#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
     颜色跟踪
"""


def process(frame):
    blur = cv.medianBlur(frame, 3)
    hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
    # 黑色
    lower = (0, 0, 0)
    upper = (180, 255, 46)
    mask = cv.inRange(hsv, lower, upper)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5), (-1, -1))
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    index = -1
    max_area = 0
    for i in range(len(contours)):
        area = cv.contourArea(contours[i])
        if max_area < area:
            max_area = area
            index = i
    if -1 != index:
        rect = cv.minAreaRect(contours[index])
        cv.ellipse(frame, rect, (255, 0, 0), 2, cv.LINE_8)
        cv.circle(frame, (np.int32(rect[0][0]), np.int32(rect[0][1])), 2, (0, 255, 0), cv.LINE_8)
    return frame


def main():
    capture = cv.VideoCapture(0)
    while True:
        ret, frame = capture.read()
        if True is not ret:
            print("can't read any video!")
            return
        dst = process(frame)
        key = cv.waitKey(20)
        if 27 == key:  # ESC
            break
        cv.imshow("catch...", dst)
    capture.release()
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
