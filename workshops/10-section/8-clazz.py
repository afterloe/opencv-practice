#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
HOG特征匹配
     1 -> 通过样本提取HOG描述子，生成样本特征数据
     2 -> svm 分类学习与训练，保存为模型
 
 HOG提取描述子
     hog.compute(image, winStride, padding)
        - image 提取图像的地址
        - winStride HOG描述子窗口大小
        - padding 填充大小 
"""


def main():
    src = cv.imread("../../../raspberry-auto/pic/Meter.jpg")
    print(src.shape)
    hog = cv.HOGDescriptor()
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    fv = hog.compute(gray, winStride=(8, 8), padding=(0, 0))
    print(len(fv))
    print(fv)
    cv.imshow("hog-descriptor", src)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
