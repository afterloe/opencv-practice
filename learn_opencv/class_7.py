#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

# 创建图像
src1 = np.zeros((400, 400, 3), np.uint8)
src1[100:200, 100:200, 1] = 255
src1[100:200, 100:200, 2] = 255
src2 = np.zeros(shape=(400, 400, 3), dtype=np.uint8)
src2[150:250, 150:250, 2] = 255

cv.imshow("src-1", src1)
cv.imshow("src-2", src2)

dst_and = cv.bitwise_and(src1, src2)  # 与操作
dst_xor = cv.bitwise_xor(src1, src2)  # 异或操作
dst_or = cv.bitwise_or(src1, src2)  # 或操作

cv.imshow("and", dst_and)
cv.imshow("xor", dst_xor)
cv.imshow("or", dst_or)

src = cv.imread("G:/pic/1.jpg")
dst_not = cv.bitwise_not(src)  # 反色, 取反操作 二值图分析中经常使用
cv.imshow("not", dst_not)

cv.waitKey(0)
cv.destroyAllWindows()
