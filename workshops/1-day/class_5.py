#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np


# 对图像进行 算数操作时要注意， 图像的数据类型、通道数、大小必须相同
src1 = cv.imread("G:/pic/1yuan.jpg")
src2 = cv.imread("G:/pic/5yuan.jpg")

add_result = np.zeros(src1.shape, src1.dtype)
cv.add(src1, src2, add_result)
cv.imshow("add_result", add_result)

# cv.subtract()  # 减
# cv.multiply()  # 乘
# cv.divide()  # 除

cv.waitKey(0)
cv.destroyAllWindows()

"""
    自己对像素点进行操作时，需要防止像素点数值越位即 每个通道内数值因 0 < value < 255 之间
"""
