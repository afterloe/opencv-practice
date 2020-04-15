#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
    使用几何矩计算轮廓中心与横纵波比对过滤
        对二值图像的各个轮廓进行计算获得对应的几何矩，根据几何矩计算轮廓点的中心位置。
        cv.moments(contours, binaryImage)
            - contours: 轮廓点集
            - binaryImage: bool, default False；二值图返回  
"""


def main():
    src = cv.imread("../../pic/money.jpg")
    cv.namedWindow("src", cv.WINDOW_KEEPRATIO)
    cv.namedWindow("dst", cv.WINDOW_KEEPRATIO)
    cv.imshow("src", src)
    t = 80
    binary = cv.Canny(src, t, t * 2)
    k = np.ones((3, 3), dtype=np.uint8)
    binary = cv.morphologyEx(binary, cv.MORPH_DILATE, k)
    contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for index in range(len(contours)):
        contour = contours[index]
        rect = cv.minAreaRect(contour)
        # cx, cy = rect[0]
        ww, hh = rect[1]
        ratio = np.minimum(ww, hh) / np.maximum(ww, hh)
        print("ratio is ", ratio)
        mm = cv.moments(contour)
        m00 = mm["m00"]
        m10 = mm["m10"]
        m01 = mm["m01"]
        cx = np.int(m10 / m00)
        cy = np.int(m01 / m00)
        box = np.int0(cv.boxPoints(rect))
        if 0.9 < ratio:
            cv.drawContours(src, [box], 0, (255, 0, 0), 2, cv.LINE_8)
            cv.circle(src, (np.int32(cx), np.int32(cy)), 2, (0, 0, 255), 2, cv.LINE_8)
        if 0.5 > ratio:
            cv.drawContours(src, [box], 0, (255, 255, 0), 2, cv.LINE_8)
            cv.circle(src, (np.int32(cx), np.int32(cy)), 2, (0, 255, 0), 2, cv.LINE_8)
    cv.imshow("dst", src)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
