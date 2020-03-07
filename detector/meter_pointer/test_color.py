#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import imutils
import time
import math
import numpy as np


"""

"""


def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def main():
    image = cv.imread("G:\\Project\\opencv-ascs-resources\\meter_pointer_roi\\2020-03-05_22-18-30.jpeg")
    # image = cv.imread("G:\\Project\\opencv-ascs-resources\\save\\box.bmp")
    start = time.time()
    image = imutils.resize(image, width=300)
    # HSV 分割
    hsv = cv.cvtColor(image.copy(), cv.COLOR_BGR2HSV)
    hsv_min = (0, 0, 0)
    hsv_max = (180, 255, 50)
    mask = cv.inRange(hsv, hsv_min, hsv_max)
    lines = cv.HoughLinesP(mask, 1, np.pi / 180, 10, None, 30, 10)
    if None is lines:
        print("未检测到直线")
        return
    line = lines[0][0]  # 检测到的直线信息
    cv.line(image, (line[0], line[1]), (line[2], line[3]), (0, 255, 255), 1, cv.LINE_AA)

    # kernel = cv.getStructuringElement(cv.MORPH_RECT, (15, 15))
    # edged = cv.morphologyEx(mask, cv.MORPH_DILATE, kernel)
    # contours, _ = cv.findContours(edged, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # contours = sorted(contours, key=cv.contourArea, reverse=True)
    # # 获取指针位置
    # x, y, w, h = cv.boundingRect(contours[0])
    # cv.circle(image, (x, y), int(calculate_distance(x, y, w, h)), (255, 0, 0), 2, cv.LINE_AA)
    # cv.line(image.copy(), (x, y), (x + w, y + h), (255, 255, 0), 2, cv.LINE_AA)

    # gray = cv.cvtColor(image.copy(), cv.COLOR_BGR2GRAY)
    # gray = cv.bilateralFilter(gray, 11, 17, 17)
    # blurred = cv.GaussianBlur(gray, (5, 5), 0)
    # threshed = cv.adaptiveThreshold(blurred, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 10)
    # cnts = cv.findContours(threshed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # cnts = imutils.grab_contours(cnts)
    # dig_cnts = []
    #
    # for cnt in cnts:
    #     x, y, w, h = cv.boundingRect(cnt)
    #     print(x, y, w, h)
    #     print("---------------------------")
    #     if 3 < h < 20 and 1 < w < 75:
    #         rect = cv.minAreaRect(cnt)
    #         cx, cy = rect[0]
    #         dig_cnts.append((x, y, w, h, cx, cy))  # 提取数字
    # for cnt in dig_cnts:
    #     x, y, w, h, cx, cy = cnt
    #     cv.rectangle(image, (x, y), (x + w, y + h), (255, 255, 0), 2, cv.LINE_8)

    print(time.time() - start)
    cv.imshow("image", image)
    # cv.imshow("threshed", threshed)
    # cv.imshow("edged", edged)
    # cv.imshow("dst", dst)
    cv.waitKey(0)

    pass


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
