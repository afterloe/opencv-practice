#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

"""
    图像直方图反向投影：
        图像直方图反向投影是通过构建指定模板图像的二维直方图空间与目标的二维直方图空间，通过直方图数据归一化后进行比率
    操作，对所有非零的数值生成对应的查找表并映射，最终对图像进行模糊输出
    
        类似于手机基站定位的原理，通常用于片段内容查找、图像目标搜寻。其工作流程如下：
            - 计算直方图
            - 计算比率R
            - LUT查找表
            - 卷积模糊
            - 归一化输出
"""


# 显示图像的 2d直方图
def hist2d(image):
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    hist = cv.calcHist([hsv], [0, 1], None, [32, 32], [0, 180, 0, 256])
    cv.imshow("image", image)
    cv.imshow("hist", hist)
    plt.imshow(hist, interpolation="nearest")
    plt.title("2D Histogram")
    plt.show()


# 直方图反向投影演示
def back_projection_demo(target):
    sample = cv.imread("../../pic/sample.png")

    # 显示2d直方图
    # hist2d(sample)
    # hist2d(target)

    roi_hsv = cv.cvtColor(sample, cv.COLOR_BGR2HSV)
    target_hsv = cv.cvtColor(target, cv.COLOR_BGR2HSV)

    # 展示效果
    cv.imshow("sample", sample)
    cv.imshow("target", target)

    roi_hist = cv.calcHist([roi_hsv], [0, 1], None, [32, 32], [0, 180, 0, 256])  # 计算直方图
    cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)  # 归一化
    dst = cv.calcBackProject([target_hsv], [0, 1], roi_hist, [0, 180, 0, 256], 1)  # 反向计算获得结果
    cv.imshow("backProjectionDemo", dst)  # 白色是感兴趣的位置
    return dst


# 显示抓取内容
def showResult(src, mask):
    canvas = cv.bitwise_and(src, src, mask=mask)  # 获取的roi与原图 进行与操作
    cv.imshow("dst", canvas)


def main():
    src = cv.imread("../../pic/money.jpg")
    dst = back_projection_demo(src)
    showResult(src, dst)
    cv.waitKey(0)
    cv.destroyAllWindows()


if '__main__' == __name__:
    main()
