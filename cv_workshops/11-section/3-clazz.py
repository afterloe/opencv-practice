#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
基于KMeans图像分割实现背景替换

步骤如下：
    1 读入图像建立KMeans样本
    2 使用KMeans图像分割，指定分类数量为4，既BGR,MASK四种
    3 选取左上角的label得到背景的cluster的索引
    4 生成mask区域，使用高斯模糊进行背景替换
"""


def main():
    image = cv.imread("../../../raspberry-auto/pic/box_04.bmp")
    h, w, ch = image.shape
    cv.imshow("input", image)
    # 构建KMeans 数据
    data = image.reshape(-1, 3)
    data = np.float32(data)
    # KMeans的终止条件
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    num_cluster = 4
    _, label, center = cv.kmeans(data, num_cluster, None, criteria, num_cluster, cv.KMEANS_RANDOM_CENTERS)
    # 生成mask区域
    index = label[0][0]  # 以第一个特征点为背景
    mask = np.zeros((h, w), dtype=np.uint8)
    label = np.reshape(label, (h, w))
    mask[label == index] = 255  # 设置背景颜色为255
    # 高斯模糊
    se = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    # 膨胀操作，将边缘扩大，防止颜色侵入
    cv.dilate(mask, se, mask)
    mask = cv.GaussianBlur(mask, (5, 5), 0)
    cv.imshow("background-mask", mask)
    # 颜色背景替换
    result = np.zeros((h, w, ch), dtype=np.uint8)
    for row in range(h):
        for col in range(w):
            w1 = mask[row, col] / 255.0  # 背景颜色识别，为背景的话颜色值为1
            w2 = 1.0 - w1
            # 颜色替换
            b, g, r = image[row, col]
            b = w1 * 255.0 + b * w2
            g = w1 * 0 + g * w2
            r = w1 * 255 + r * w2
            result[row, col] = (b, g, r)
    cv.imshow("background substitution", result)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
