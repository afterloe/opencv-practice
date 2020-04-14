#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    中值滤波：
        用于去除图像中的"椒盐噪声"，属于统计排序滤波器中的一种，是常见的图像去噪声与增强的方式之一。
    其原理采用窗口在图像上移动，对覆盖区域下的所有像素进行排序，并对卷积中心的像素值修改为排序后后的中间值，故
    称为中值滤波。
"""


def main():
    src = cv.imread("../../pic/IMG_20191204_151013.jpg")
    cv.namedWindow("src", cv.WINDOW_AUTOSIZE)
    cv.imshow("src", src)
    # 由于中值滤波采用排序的方式对周边像素进行处理，故 ksize 必须大于1且为奇数
    dst = cv.medianBlur(src, 15)
    cv.imshow("dst", dst)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
