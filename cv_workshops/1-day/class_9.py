#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

gray = cv.imread("../../pic/gray.png", cv.IMREAD_GRAYSCALE)
cv.imshow("gray", gray)

min_v, max_v, min_loc, max_loc = cv.minMaxLoc(gray)
print("min: %.3f, max: %.3f" % (min_v, max_v))
print("min loc: ", min_loc)
print("max loc: ", max_loc)

# means - 均值； stddev - 标准方差
means, stddev = cv.meanStdDev(gray)
print("mean: %.3f, stddev: %.3f" % (means, stddev))

# 二值化处理（以均值为界限， 小于均值的设置为0，大于均值的设置为255）
gray[np.where(gray < means)] = 0
gray[np.where(gray > means)] = 255

cv.imshow("binary", gray)

print("------------------------------->>> 3 channel pic")

src = cv.imread("../../pic/rmb/100.png")
cv.imshow("input", src)

# 3通道图片是不能做 最小像素、最大像素与位置
# min_v, max_v, min_loc, max_loc = cv.minMaxLoc(src)
# print("min: %.3f, max: %.3f" % (min_v, max_v))
# print("min loc: ", min_loc)
# print("max loc: ", max_loc)

# 3通道图片 每个数组的 均值和 极值是不一样的
means_arr, stddev_arr = cv.meanStdDev(src)
print("blue channel ->> mean: %.3f, stddev: %.3f" % (means_arr[0], stddev_arr[0]))
print("green channel ->> mean: %.3f, stddev: %.3f" % (means_arr[1], stddev_arr[1]))
print("red channel ->> mean: %.3f, stddev: %.3f" % (means_arr[2], stddev_arr[2]))


cv.waitKey(0)
cv.destroyAllWindows()
