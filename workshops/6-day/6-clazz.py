#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
    点多边形检测
        对于轮廓图像， 判断点是否在轮廓内，在opencv被称为点多边形检测，通过该api可以获得点到轮廓的距离。该api也被用于车辆压线判断等多
    个场景。
    
    cv.pointPolygonTest(contours, point, measureDist)
        - contours: 轮廓点集
        - point：检测点
        - measureDist: bool， True 返回点到轮廓的距离； False 返回1，0，-1，表示在轮廓内，轮廓边缘上、轮廓外
"""


def main():
    src = cv.imread("../../pic/mask.png")
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_TRIANGLE)
    cv.imshow("src", binary)
    image = np.zeros(src.shape, dtype=np.float32)
    contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    h, w = image.shape[:2]
    for row in range(h):
        for col in range(w):
            dist = cv.pointPolygonTest(contours[0], (col, row), True)
            if 0 == dist:
                image[row, col] = (255, 255, 255)
            if 0 > dist:
                image[row, col] = (0, 0, 255 + dist)
            if 0 < dist:
                image[row, col] = (255 - dist, 0, 0)
    dst = cv.convertScaleAbs(image)
    dst = np.uint8(dst)
    cv.imshow("dst", dst)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
