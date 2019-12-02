#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv

src = cv.imread("../../pic/rmb/100.png", cv.IMREAD_COLOR)
cv.imshow("src", src)

"""
    flip 图像翻转用于 视频采集或 拍摄过程中对 视频进行翻转，如android的前置相机
"""
dst = cv.flip(src, flipCode=0)  # X轴翻转， 上下对称
cv.imshow("x-flip", dst)

cv.flip(src, 1, dst)  # Y轴翻转， 左右对称
cv.imshow("y-flip", dst)

cv.flip(src, -1, dst)  # XY轴翻转， 对角线对称
cv.imshow("xy-flip", dst)

cv.waitKey(0)
cv.destroyAllWindows()
