#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    图像直方图比较：
        图像直方图比较是就按特定几类算法对两幅图像的直方图数据进行相似性比较，获得两幅图像间的相似程度
    0——HISTCMP_CORREL  相关性   越接近1表示越像
    1——HISTCMP_CHISQR   卡方  越接近0表示越像 
    2——HISTCMP_INTERSECT  交集法  数值越大表示越像
    3——HISTCMP_BHATTACHARYYA 常态分布比对的BHATTACHARYYA距离法 越接近0表示越像
    
    比较步骤：
        将图像转换为hsv色系
        取hsv色系中的hs两个通道计算直方图
        将直方图进行归一化处理
        直方图对比
"""


src1 = cv.imread("../../pic/5yuan.jpg")
src2 = cv.imread("../../pic/rmb/5.png")
src3 = cv.imread("../../pic/IMG_20191204_151145.jpg")
src4 = cv.imread("../../pic/1.jpg")

cv.imshow("src1", src1)
cv.imshow("src2", src2)
cv.imshow("src3", src3)
cv.imshow("src4", src4)

# 使用hsv 色系对 直方图统计与匹配更加 标准
hsv1 = cv.cvtColor(src1, cv.COLOR_BGR2HSV)
hsv2 = cv.cvtColor(src2, cv.COLOR_BGR2HSV)
hsv3 = cv.cvtColor(src3, cv.COLOR_BGR2HSV)
hsv4 = cv.cvtColor(src4, cv.COLOR_BGR2HSV)

# 计算直方图， 对于 hsv色系， hs两个通道的值较具有比较意义;
# rang 60 64 双通道的 bins的值
hist1 = cv.calcHist([hsv1], [0, 1], None, [60, 64], [0, 180, 0, 256])
hist2 = cv.calcHist([hsv2], [0, 1], None, [60, 64], [0, 180, 0, 256])
hist3 = cv.calcHist([hsv3], [0, 1], None, [60, 64], [0, 180, 0, 256])
hist4 = cv.calcHist([hsv4], [0, 1], None, [60, 64], [0, 180, 0, 256])

# 归一化处理, 进行比较
cv.normalize(hist1, hist1, 1.0, 1.0, cv.NORM_INF)
cv.normalize(hist2, hist2, 1.0, 1.0, cv.NORM_INF)
cv.normalize(hist3, hist3, 1.0, 1.0, cv.NORM_INF)
cv.normalize(hist4, hist4, 1.0, 1.0, cv.NORM_INF)

# 常用的方法有以下四种
methods = [cv.HISTCMP_CORREL, cv.HISTCMP_CHISQR, cv.HISTCMP_INTERSECT, cv.HISTCMP_BHATTACHARYYA]

str_method = ""

# 最常用的是 相关性 或 巴式距离 计算
for method in methods:
    v1 = cv.compareHist(hist1, hist2, method)  # 图像直方图比较
    v2 = cv.compareHist(hist3, hist4, method)
    if method == cv.HISTCMP_CORREL:
        # 相关性计算， 值越接近1 表示越像
        str_method = "Correlation 相关性"
    if method == cv.HISTCMP_CHISQR:
        # 卡方计算方式，值越接近0表示越像
        str_method = "Chi-square 卡方"
    if method == cv.HISTCMP_INTERSECT:
        # 交叉 数字越大表示越像
        str_method = "Intersection 交叉"
    if method == cv.HISTCMP_BHATTACHARYYA:
        # 巴氏 越接近0表示越像
        str_method = "Bhattacharyya 巴式"
    print("%s v1 = %.4f, v2 = %.4f" % (str_method, v1, v2))

cv.waitKey(0)
cv.destroyAllWindows()