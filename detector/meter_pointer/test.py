#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import imutils
import math
import numpy as np

"""

"""


def t(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def main():
    image = cv.imread("G:\\Project\\opencv-ascs-resources\\meter_pointer_roi\\2020-03-05_22-18-30.jpeg")
    image = imutils.resize(image, width=500)
    h, w = image.shape[: 2]
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.bilateralFilter(gray, 11, 17, 17)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    threshed = cv.adaptiveThreshold(blurred, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 10)
    lines = cv.HoughLinesP(threshed, 1, np.pi / 180, 180, None, 100, 10)

    cv.circle(image, (np.int32(w // 2), np.int32(h // 2)), 2, (255, 0, 0), 2, cv.LINE_8)

    if None is lines:
        print("未检测到直线")
        return
    near = None
    dist = h
    for index in range(len(lines)):
        line = lines[index][0]  # 检测到的直线信息
        # print(line[:4])
        d = t(line[2], line[3], w, h)
        # print(d)
        if d < dist:
            dist = d
            near = line[:4]
    # 指针已出
    cv.line(image, (near[0], near[1]), (near[2], near[3]), (255, 0, 0), 1, cv.LINE_AA)
    cnts = cv.findContours(threshed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # for cnt in cnts:
    # x, y, w, h = cv.boundingRect(cnt)
    # if w >= 150 and 100 < h < 200:
    # cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv.imshow("target", image)
    cv.imshow("threshed", threshed)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
