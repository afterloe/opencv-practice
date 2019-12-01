#!/usr/bin/env python
# -*- coding==utf-8 -*-

import cv2 as cv
import numpy as np

src = cv.imread("G:/pic/1.jpg")
m1 = np.copy(src)  # 克隆图像

m2 = src  # 赋值图像
src[100:200, 200:300, :] = 0
cv.imshow("m2", m2)

# 创建空白图像， 以src 为模板进行创建
m3 = np.zeros(src.shape, src.dtype)  # shape - width * height  通道， dtype - 每个通道内的字节类型
cv.imshow("m3", m3)

m4 = np.zeros([512, 512], np.uint8)
cv.imshow("m4", m4)

m5 = np.ones(shape=[512, 512, 3], dtype=np.uint8)
m5[:, :, 0] = 255
cv.imshow("m5", m5)

cv.waitKey(0)
cv.destroyAllWindows()
