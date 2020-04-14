#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

src = cv.imread("G:/pic/1.jpg")
cv.imshow("input", src)

h, w, ch = src.shape  # 获取图像的 高、 宽、 通道属性
# ! 注意： 如果是 灰度图像，是没有 ch的值
print("h, w, ch", h, w, ch)

for row in range(h):
    for col in range(w):
        b, g, r = src[row, col]  # 获取图像中 三通道的值
        b = 255 - b
        g = 255 - g
        r = 255 - r
        src[row, col] = [b, g, r]  # 对图像像素进行取反操作

cv.imshow("output", src)
cv.waitKey(0)
cv.destroyAllWindows()

