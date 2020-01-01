#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    图像均值与高斯模糊
   
    cv.GaussianBlur 
        - kszie 卷积核大小，越大，图像越模糊 (奇数)
        - sigmaX 模糊参数，越大， 图像越模糊
        当size为0，0时， 从sigmaX开始计算
"""


def main():
    src = cv.imread("../../pic/money.jpg")
    cv.namedWindow("src", cv.WINDOW_AUTOSIZE)
    cv.imshow("src", src)
    dst1 = cv.blur(src, (5, 5))
    dst2 = cv.GaussianBlur(src, (5, 5), 0)
    dst3 = cv.GaussianBlur(src, (0, 0), sigmaX=15)
    cv.imshow("blur", dst1)
    cv.imshow("gaussian ", dst2)
    cv.imshow("gaussian sigmaX=15", dst3)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
