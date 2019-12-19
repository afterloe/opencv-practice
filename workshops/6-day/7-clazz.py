#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
    霍夫直线检测
        霍夫变换是一种图像变换算法，将二维空间坐标系变换到极坐标空间，可提取图像中的直线、圆等内容。opencv中的api如下：
        cv.HoughLines(binary, rho, theta, threshold, srn, stn, min_theta, max_theta)
            - binary: 二值图，轮廓不宜多并且噪声处理后
            - rho: 极坐标r的步长
            - theta: 角度步长
            - threshold: 累加器阈值
            - srn, stn: 多尺度霍夫变换时的参数，经典霍夫变换则不需要
            - min_theta: 直线旋转最小角度
            - max_theta: 直线旋转最大角度
"""


def main():
    src = cv.imread("../../pic/sudoku.png")
    # blur = cv.medianBlur(src, 15)
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    T = 80
    binary = cv.Canny(gray, T, T * 2)
    lines = cv.HoughLines(binary, 1, np.pi / 180, 150, None, 0, 0)
    if None is lines:
        print("未检测到直线")
        return
    for i in range(len(lines)):
        rho = lines[i][0][0]
        theta = lines[i][0][1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * a))
        pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * a))
        cv.line(src, pt1, pt2, (255, 0, 0), 3, cv.LINE_AA)
    cv.imshow("dst", src)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
