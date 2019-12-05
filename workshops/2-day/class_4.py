#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    图像插值：用于几何变换（图像放大、缩小等操作）、透视变换、插值计算新像素。
    常用的算法为以下四种：
        临近点插值算法 - 速度快
        双线性插值
        lanczos插值 - 提升精准度
        双立方插值 - 高精准，抗锯齿

    清晰度逐渐提升，
"""

src = cv.imread("../../pic/rmb/1.png", cv.IMREAD_COLOR)
h, w = src.shape[:2]  # 从0 开始，取两位; shape[h, w, ch]

print("image is %d * %d" % (h, w))

dst = cv.resize(src, (w * 2, h * 2), interpolation=cv.INTER_NEAREST)  # 临近点算法
cv.imshow("NEAREST", dst)

dst = cv.resize(src, (w * 2, h * 2), interpolation=cv.INTER_LINEAR)  # 双线性插值算法
cv.imshow("LINEAR", dst)

dst = cv.resize(src, (w * 2, h * 2), interpolation=cv.INTER_LANCZOS4)  # lanczos4插值算法
cv.imshow("LANCZOS4", dst)

dst = cv.resize(src, (w * 2, h * 2), interpolation=cv.INTER_CUBIC)  # 双立方插值算法
cv.imshow("CUBIC", dst)

cv.waitKey(0)
cv.destroyAllWindows()
