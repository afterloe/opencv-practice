#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv

src = cv.imread("G:/pic/1.jpg")
cv.imshow("src", src)

hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)  # HSV 算法模型中常用的颜色色域
cv.imshow("hsv", hsv)

yuv = cv.cvtColor(src, cv.COLOR_BGR2YUV)  # android 中相机拍摄出的颜色色域
cv.imshow("yuv", yuv)

ycrcb = cv.cvtColor(src, cv.COLOR_BGR2YCrCb)  # 人体肌肤色域
cv.imshow("ycrcb", ycrcb)

# 颜色抠图
hsv_min = (156, 43, 46)  # 红色 hsv 最小值
hsv_max = (180, 255, 255)  # 红色 hsv 最大值
mask = cv.inRange(hsv, hsv_min, hsv_max)
cv.imshow("mask - red", mask)
dst = cv.bitwise_and(src, src, mask=mask)  # bitwise_not 可以去除目标颜色， 显示底部
cv.imshow("dst", dst)

cv.waitKey(0)
cv.destroyAllWindows()
