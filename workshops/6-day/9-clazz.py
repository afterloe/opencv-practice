#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    霍夫圆检测
        根据极坐标，圆上任意一点的坐标可以表示为（x0, y0），圆半径已知，旋转360度可获取极坐标上的所有坐标；如果只知道图像上像素点，圆
    半径旋转360则中心点处的坐标值必定最强，
        cv.HoughCircles(binary, method, dp, minDist, param1, param2, minRadius, maxRadius)
            - binary: 二值图（高斯模糊后的灰度图像） 
            - method: 圆检测的方法（霍夫梯度）
            - dp: 表示图像分辨率是否变化， 为1 表示不变化， 2表示为原来的一半
            - minDist: 两个圆心间的最小距离，用于消除同心圆的情况
            - param1: 边缘提取的高阈值
            - param2: 边缘提取的低阈值
            - mainRadius: 检测圆的最小半径
            - maxRadius: 检测圆的最大半径
"""


def main():
    src = cv.imread("../../pic/euro_silver_coin.png")
    cv.namedWindow("dst", cv.WINDOW_KEEPRATIO)
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (9, 9), 2)
    circles = cv.HoughCircles(blur, cv.HOUGH_GRADIENT, 2, 100, None, 100, 80, 20, 100)
    for c in circles[0, :]:
        print(c)
        cx, cy, r = c
        cv.circle(src, (cx, cy), 2, (255, 0, 0), 2, cv.LINE_8)
        cv.circle(src, (cx, cy), r, (0, 255, 0), 2, cv.LINE_8)
    cv.imshow("dst", src)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
