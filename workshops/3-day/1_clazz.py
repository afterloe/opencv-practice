#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    图像卷积操作：
        图像卷积可以理解为一个窗口区域在另一个大的图像上移动，对每个覆盖区域进行点乘操作，最终获得中心像素的输出值。
"""


def main():
    src = cv.imread("../../pic/sample.png")
    cv.namedWindow("input", cv.WINDOW_AUTOSIZE)
    cv.imshow("input", src)
    # 卷积操作api
    # - input： 输入
    # - out： dst 输出
    # - size： 卷积窗口大小
    # - point： 中心像素位置 (-1, -1)
    dst = cv.blur(src, (15, 15))
    cv.imshow("blur", dst)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
