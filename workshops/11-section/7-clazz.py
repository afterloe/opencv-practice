#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
图像均值漂移分割
    图像均值漂移分割是一种无监督的图像分割方法，对于图像多维度数据颜色值(RGB)与空间位置(x,y)，所以需要两个窗口半径，一个是空间半径、另外一个
是颜色半径，经过均值漂移窗口的所有的像素点会具有相同的像素值，OpenCV中均值漂移分割的API如下:

cv.pyrMeanShiftFiltering(src, dst, sp, sr, maxLevel, criteria)
    - src 输入图像
    - dst 输出图像
    - sp 空间窗口大小
    - sr 颜色空间大小
    - maxLevel 金字塔层数，总层数为maxlevel + 1
    - criteria 停止条件
"""


def main():
    image = cv.imread("../../../raspberry-auto/pic/49a1f637jw1evzjx6ljr6j213l1gshdt.jpg")
    cv.imshow("input", image)
    dst = cv.pyrMeanShiftFiltering(image, 25, 40, None, 2)
    cv.imshow("result", dst)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
