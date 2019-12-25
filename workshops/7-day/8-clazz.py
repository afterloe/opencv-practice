#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    形态学分析 - 图像梯度
        形态学分析可以忽略颜色、光照的效果，提取连通组件的边缘与轮廓，根据形态学操作的不同，形态学梯度分为以下几种:
            基本梯度： 原理为膨胀减腐蚀之间的差值, opencv中morphologyEx操作，option枚举 MORPH_GRADIENT
            内梯度： 原理为输入图像与腐蚀之间的差值，opencv中并没有实现，需要自己编码
            外梯度： 原理为膨胀与输入图像之间的差值，opencv中并没有实现，需要自己编码
"""


def out_gradient(src):
    # 外梯度为 膨胀图像 与 输入图像的差值
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    binary = cv.dilate(src, kernel)
    dst = cv.subtract(binary, src)
    return dst


def inner_gradient(src):
    # 内梯度为 输入图像与腐蚀图像的差值
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    binary = cv.erode(src, kernel)
    dst = cv.subtract(src, binary)
    return dst


def main():
    src = cv.imread("../../pic/1.jpg")
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    cv.imshow("src", gray)
    blur = cv.medianBlur(gray, 3)
    # 基本梯度
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    dst_1 = cv.morphologyEx(blur, cv.MORPH_GRADIENT, kernel)
    cv.imshow("morph_gradient", dst_1)
    dst_2 = inner_gradient(blur)
    cv.imshow("morph_inner_gradient", dst_2)
    dst_3 = out_gradient(blur)
    cv.imshow("morph_out_gradient", dst_3)
    # canny 结果 - 干扰比较多
    dst_4 = cv.Canny(blur, 80, 160)
    cv.imshow("canny", dst_4)
    # threshold 结果  - 受颜色、光照、拍摄设备等影响比较多
    _, dst_5 = cv.threshold(blur, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    cv.imshow("threshold", dst_5)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
