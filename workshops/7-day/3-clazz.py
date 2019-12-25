#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    形态学操作 - 开操作
        开操作 = 腐蚀 + 膨胀
        opencv关于形态学操作进行了封装，所有的形态学操作可使用一个api进行，即
        cv.morphologyEx(src, option, kernel, anchor, iterations)
            - src: 任意输入图像，可以为灰度、彩色或二值
            - option: 形态学操作的枚举
            - kernel: 结构元素 或 卷积核
            - anchor: 结构元素或卷积核的中心像素点坐标
            - iterations: 形态学操作的次数
            
        关于开操作可以理解如下，先对图像进行腐蚀操作，之后对腐蚀的结果进行膨胀。可以删除二值图像中的干扰快，降低图像二值化之后噪点过多的
    问题，在api中，他的枚举为`cv.MORPH_OPEN`
"""


def main():
    src = cv.imread("../../pic/cement_road.jpeg")
    cv.namedWindow("binary", cv.WINDOW_KEEPRATIO)
    cv.namedWindow("dst", cv.WINDOW_KEEPRATIO)
    cv.namedWindow("src", cv.WINDOW_KEEPRATIO)
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (3, 3), 0)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    binary = cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 10)
    dst = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)
    cv.imshow("binary", binary)
    cv.imshow("dst", dst)
    cv.imshow("src", src)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
