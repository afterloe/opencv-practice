#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv
from matplotlib import pyplot as plt

"""
    颜色直方图：
        颜色直方图是图像像素统计学特征，计算代价小，具有图像平移、旋转、缩放不变性等众多有点，广泛运用于图像处理的各个领
    域，特别是灰度图像的阀值分割、基于颜色的图像检索以及图像分类、反向投影跟踪。常见的分为灰度直方图与颜色直方图。
    
        其中， bins指直方图的大小范围，像素取值在[0, 255]之间，最少256个bin，此外还可以有 16, 32, 64, 128等，256整数倍的
    值。
"""


# 灰度图像的直方图
def image_gray_hist(gray):
    cv.namedWindow("input-gray", cv.WINDOW_KEEPRATIO)
    cv.imshow("input-gray", gray)
    # cv2.calcHist(images, channels, mask, histSize, ranges[, hist[, accumulate ]]) #返回hist
    # 第一个参数必须用方括号括起来。
    # 第二个参数是用于计算直方图的通道， 也必须用方括号括起来
    # 第三个参数是Mask
    # 第四个参数是histSize，表示这个直方图分成多少份（即多少个直方柱）。
    # 第五个参数是表示直方图中各个像素的值
    hist = cv.calcHist([gray], [0], None, [256], [0, 256])
    plt.figure()
    plt.title("Grayscale Histogram")
    plt.xlabel("Bins")
    plt.ylabel("# of Pixels")
    plt.plot(hist)
    plt.xlim([0, 256])
    plt.show()


# 彩色图像的 直方图
def image_hist(img):
    cv.imshow("input", img)
    color = ("blue", "green", "red")
    for i, color in enumerate(color):
        hist = cv.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(hist, color=color)
        plt.xlim([0, 256])
    plt.show()


src = cv.imread("../../pic/IMG_20191204_151145.jpg")
gray_pic = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
# cv.imshow("input", gray_pic)
# image_hist(src)
image_gray_hist(gray=gray_pic)
cv.waitKey(0)
cv.destroyAllWindows()
