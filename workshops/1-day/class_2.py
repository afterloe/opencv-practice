#!/usr/bin/env python
# -*- coding=utf-8 -*-

"""
    create by afterloe on 2019-12-01
    version is 1.0.0
"""

import cv2 as cv


"""
    COLOR_BGR2GRAY = 6 彩色到灰度
    COLOR_GRAY2BGR = 8 灰度到彩色
    COLOR_BGR2HSV = 40 BGR到HSV
    COLOR_HSV2BGR = 54 HSV到BGR
"""
src = cv.imread("G:/pic/5yuan.jpg")
cv.namedWindow("input", cv.WINDOW_AUTOSIZE)
cv.imshow("input", src)
gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)  # 颜色转换
cv.imshow("gray", gray)
cv.waitKey(0)
cv.destroyAllWindows()

cv.imwrite("G:/pic/gray.png", gray)  # 保存图片 src 为目录， mat为 图像
