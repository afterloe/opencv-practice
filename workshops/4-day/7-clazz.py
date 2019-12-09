#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    图像金字塔：
        对一张输入图像进行模糊操作后，再进行采样，大小为原图的1/4 （即宽高缩小一半）
            reduce 从原图生成一系列低分辨率图像（逐步缩小）py.pyrDown
            expand 从原图生成一系列高分辨率图像（逐步放大）py.pyrUp
        图像金字塔必须逐层操作且每次操作后结果都是前一层的1/4
"""


# 金字塔向上走 - 逐步缩小
def pyramid_up(image, level=3):
    temp = image.copy()
    pyramid = []
    for i in range(level):
        dst = cv.pyrDown(temp)
        pyramid.append(dst)
        temp = dst.copy()
    return pyramid


# 金字塔向下走 - 逐步放大
def pyramid_down(image, level=3):
    temp = image.copy()
    pyramid = []
    for i in range(level):
        dst = cv.pyrUp(temp)
        pyramid.append(dst)
        temp = dst.copy()
    return pyramid


def show(pyramid):
    for i in range(len(pyramid)):
        cv.imshow(str(i), pyramid[i])
    cv.waitKey(0)
    cv.destroyAllWindows()


def main():
    src = cv.imread("../../pic/3.png")

    # 金字塔向上 - 图像逐步缩小
    result = pyramid_up(src)
    show(result)

    # 金字塔向下 - 图像逐步放大
    src = cv.imread("../../pic/luoxiaohe.jpg")
    result = pyramid_down(src)
    show(result)


if "__main__" == __name__:
    main()
