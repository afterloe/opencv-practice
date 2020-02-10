#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
HOG 特征与行人检测
    HOG特征在对象识别模式与模式匹配中是一种常见的特征提取算法，是基于本地像素块特征直方图提取的一种算法，对象局部的变形与
光照影响有很好的稳定性，最初使用HOG特征与SVM训练可以得到很好的效果。

HOG特征检测的相关步骤
    输入图像 -> Gramma校正 -> 灰度化处理 -> 计算XY梯度 -> 8x8网格方向梯度权重直方图统计 -> 块描述与特征向量归一化

API描述(部分)
    HOG.detectMultiScale(img, foundLocations, winStride, padding, scale, useMeanshiftGrouping)
        - img 需要搜索的图像
        - foundLocations 发现对象的矩阵形框
        - winStride 开窗计算的窗口大小, 整数
        - padding 填充大小
        - scale 尺度空间
        - useMeanshiftGrouping 是否分组算法， 不建议用 速度太慢
"""

hog_param = {"winStride": (1, 1), "padding": (1, 1), "scale": 1.5, "useMeanshiftGrouping": False}


def main():
    pic = cv.imread("../../../raspberry-auto/pic/10-section-7.png")
    cv.imshow("src", pic)
    hog = cv.HOGDescriptor()
    hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())
    hog_param["img"] = pic
    (results, weight) = hog.detectMultiScale(**hog_param)
    for (x, y, w, h) in results:
        cv.rectangle(pic, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv.imshow("dst", pic)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
