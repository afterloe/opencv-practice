#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
    二值图像分析 - 读取最大轮廓与编码关键点
        获取二值化后的图像进行轮廓分析，根据面积寻找最大轮廓，然后根据轮廓进行轮廓逼近，获取关键点轮廓点。
"""


def contour_process(src, contours):
    height, width = src.shape[:2]
    # 提取最大轮廓
    i = 0
    max_value = 0
    for index in range(len(contours)):
        contour = contours[index]
        x, y, w, h = cv.boundingRect(contour)
        if height <= h or width <= w:
            continue
        area = cv.contourArea(contour)
        if area > max_value:
            max_value = area
            i = index
    result = np.zeros(src.shape, dtype=np.uint8)
    key_pts = cv.approxPolyDP(contours[i], 4, True)
    cv.drawContours(src, contours, i, (0, 0, 255), 2, cv.LINE_8)
    cv.drawContours(result, contours, i, (0, 0, 255), 2, cv.LINE_8)
    for pt in key_pts:
        cv.circle(src, (pt[0][0], pt[0][1]), 2, (255, 0, 0), 2, cv.LINE_8)
        cv.circle(result, (pt[0][0], pt[0][1]), 2, (255, 0, 0), 2, cv.LINE_8)
    cv.imshow("dst", src)
    cv.imshow("result", result)


def main():
    src = cv.imread("../../../raspberry-auto/pic/case6.jpg")
    cv.imshow("src", src)
    blur = cv.medianBlur(src, 3)
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)  # 全局阈值二值化
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    # binary = cv.morphologyEx(gray, cv.MORPH_GRADIENT, kernel)
    cv.imshow("binary", binary)
    binary = cv.morphologyEx(binary, cv.MORPH_CLOSE, kernel)
    contours, _ = cv.findContours(binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    contour_process(src, contours)
    cv.waitKey(0)
    cv.destroyAllWindows()


def main_1():
    src = cv.imread("../../../raspberry-auto/pic/case6.jpg")
    blur = cv.medianBlur(src, 3)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    gradient = cv.morphologyEx(blur, cv.MORPH_GRADIENT, kernel)
    gray = cv.cvtColor(gradient, cv.COLOR_BGR2GRAY)
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)

    contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contour_process(src, contours)
    cv.imshow("dst", binary)
    cv.imshow("src", src)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    # main_1()
    main()
