#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    形态学操作 - 图像的膨胀与腐蚀
        图像的膨胀与腐蚀是形态学中的两个最基本的操作，opencv中膨胀与腐蚀均有特定的api来实现。简单而言，膨胀可以看成最大值滤波，即使用八
    领域或四领域中像素最高值与中心点进行替换；而腐蚀可以看做是最小值滤波，原理同上。其实，在膨胀与腐蚀中的kernel指的并不是卷积核，他应该
    被成为结构元素，也就是说可以使用非矩形的卷积操作。具体的api如下：
    膨胀 cv.dilate(src, kernel, anchor, iterations)
        - src: 灰度图相关或bgr图像均可
        - kernel: 结构元素
        - anchor: 中心像素点
        - iterator: default 1， 循环次数
        
    腐蚀 cv.erode(src, kernel, anchor, iterations)
        - 同上
"""


def main():
    src = cv.imread("../../pic/hand.jpg")
    cv.namedWindow("src", cv.WINDOW_KEEPRATIO)
    cv.namedWindow("dilate", cv.WINDOW_KEEPRATIO)
    cv.namedWindow("erode", cv.WINDOW_KEEPRATIO)
    # blur = cv.medianBlur(src, 15)
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3), (-1, -1))  # 获取结构元素
    dilate = cv.dilate(gray, kernel)
    erode = cv.erode(gray, kernel)
    cv.imshow("src", gray)
    cv.imshow("dilate", dilate)
    cv.imshow("erode", erode)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
