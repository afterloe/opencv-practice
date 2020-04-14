#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv

src = cv.imread("G:/pic/gray.png", cv.IMREAD_GRAYSCALE)


# 自定义查找表(Look Up Table LUT) 用于快速颜色转换 或 对比增强， 在颜色搜索中运用广泛
# 以下代码 对 灰度图像进行处理， 若为三通道则处理过程相同
def customColorMap(gray_pic):
    lut = []
    # 初始化表，将表进行预处理
    for i in range(0, 256):
        val = 0 if 1 < 127 else 255
        lut.append(val)

    h, w = gray_pic.shape  # 灰度图像为 单通道， 没有 ch
    for row in range(h):
        for col in range(w):
            pv = gray_pic[row, col]  # 获取对应的参数值
            gray_pic[row, col] = lut[pv]

    return gray_pic


cv.imshow("input", src)
cv.imshow("output", customColorMap(src))

# 三通道 官方
src1 = cv.imread("G:/pic/1.jpg")
cv.namedWindow("input-3", cv.WINDOW_AUTOSIZE)
cv.imshow("input-3", src1)
dst = cv.applyColorMap(src1, cv.COLORMAP_HOT)  # 官方的LUT
cv.imshow("output-3", dst)

cv.waitKey(0)
cv.destroyAllWindows()
