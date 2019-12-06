#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    边缘保留滤波算法 - 快速滤波
        该算法采用降纬运算的原理，提升了高斯双边及mean shift均值迁移的运算速度。
        
    edgePreservingFilter(src, dst, flags, sigma_s, sigma_r)
        flags - 1
        sigma_s - 取值范围0 ~ 200;
        sigma_r - 取值范围0 ~ 1;
        
        当sigma_s 取值不变时， sigma_r 越大，图像过滤效果越明显
        当sigma_r 取值不变时， sigma_s 越大，图像过滤效果越明显
        当sigma_r 取值太小时，无论sigma_s 如何变化，图像过滤效果均不符合效果
"""


def main():
    src = cv.imread("../../pic/IMG_20191204_151110.jpg")
    cv.namedWindow("src", cv.WINDOW_AUTOSIZE)
    cv.imshow("src", src)
    dst = cv.edgePreservingFilter(src, sigma_s=100, sigma_r=0.4, flags=cv.RECURS_FILTER)
    cv.imshow("dst", dst)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
