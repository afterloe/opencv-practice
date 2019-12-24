#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    图像的膨胀与腐蚀
        图像形态学操作不仅可以对二值图像操作，也可以对灰度图像与彩色图像进行操作。对于二值图像的膨胀与腐蚀而言，选择一个好的结构元素是至
    关重要的，Opencv中关于结构元素的获取有一个api，具体如下：
        cv.getStructuringElement(shape, ksize, anchor)
            - shape: 结构元素的形状，常用的有矩形、圆形、十字交叉
            - ksize: 结构元素的大小
            - anchor: 结构元素的中心像素点的位置
        在二值图像中，膨胀可以将二值图像的轮廓进行扩充，实现两个连通组件因为某些像素中断导致的组件分离。而腐蚀刚好相反。
"""


def main():
    src = cv.imread("../../pic/money.jpg")
    cv.namedWindow("binary", cv.WINDOW_KEEPRATIO)
    cv.namedWindow("dilate", cv.WINDOW_KEEPRATIO)    # 膨胀
    cv.namedWindow("erode", cv.WINDOW_KEEPRATIO)    # 腐蚀
    blur = cv.medianBlur(src, 15)
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)    # 灰度图像才能寻找均值
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))  # 创建一个3*3 的矩形结构元素
    dilate = cv.dilate(binary, kernel)
    erode = cv.erode(binary, kernel)
    cv.imshow("binary", binary)
    cv.imshow("dilate", dilate)
    cv.imshow("erode", erode)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
