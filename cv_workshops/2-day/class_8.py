#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv
from matplotlib import pyplot as plt


def image_gray_hist(gray, name_window="input-gray"):
    hist = cv.calcHist([gray], [0], None, [256], [0, 256])
    plt.figure()
    plt.title(name_window)
    plt.xlabel("Bins")
    plt.ylabel("# of Pixels")
    plt.plot(hist)
    plt.xlim([0, 256])
    plt.show()


src = cv.imread("../../pic/1yuan.jpg")
gray_pic = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
# 图像直方均衡化用于图像增强， 对输入图像进行直方图均衡化处理，提升其他类库对对象检测的准确率；
# 该算法在医学影像图像与卫星遥感影像处理上均有使用，被用于提升输入图像的质量
dst = cv.equalizeHist(gray_pic)  # 图像直方图均衡化

# 对均衡前后的 图像直方图进行对比
image_gray_hist(gray_pic, "before")
image_gray_hist(dst, "after")
# 均衡后所有像素点均匀分分布，提升部分均值

cv.waitKey(0)
cv.destroyAllWindows()
