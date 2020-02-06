#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

"""
KMeans数据分类
     K-Means的算法是对数据进行分类的算法，采用的硬分类方式，是属于非监督学习的算法，预先要求知道分为几个类别，然后每个类别有一
个中心点，根据距离度量来决定每个数据点属于哪个类别标签，一次循环实现对所有数据点分类之后，会根据标签重新计算各个类型的中心位置，
然后继续循环数据集再次分类标签样本数据，如此不断迭代，直到指定的循环数目或者前后两次delta小于指定阈值，停止计算，得到最终各个样
本数据的标签

相关API
cv.kmeans(data, K, bestLabels, criteria, attempts, flags, centers)
    - data 输入的样本数据(必须是行组织样本，每一行为一个样本数据，列表表示样本的维度)\
    - K 最终的分类数目
    - bestLabels 表示最终分类每个样本的标签
    - criteria 表示KMeans分割的停止条件
    - attempts 采用不同初始化标签尝试次数
    - flags 中心初始化方法
        > KMEANS_RANDOM_CENTERS
        > KMEANS_PP_CENTERS
        > KMEANS_USE_INITIAL_LABELS
    - centers 最终分割后每个cluster的中心位置
"""


def main():
    # 初始化样本数据
    x = np.random.randint(25, 50, (25, 2))
    y = np.random.randint(60, 85, (25, 2))
    pts = np.vstack((x, y))

    data = np.float32(pts)
    print(data.shape)
    # 终止条件
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv.kmeans(data, 2, None, criteria, 2, cv.KMEANS_RANDOM_CENTERS)
    print(len(label))
    print(center)

    a = data[label.ravel() == 0]
    b = data[label.ravel() == 1]
    # 采用直方图形式进行结果展示
    plt.scatter(a[:, 0], a[:, 1])
    plt.scatter(b[:, 0], b[:, 1], c='r')
    plt.scatter(center[:, 0], center[:, 1], s=80, c='y', marker='s')
    plt.xlabel('Height')
    plt.ylabel('Weight')
    plt.show()


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
