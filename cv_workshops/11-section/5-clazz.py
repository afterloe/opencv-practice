#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
OpenCV中机器学习模块的最近邻算法KNN， 对使用KNN训练好的XML文件，可以通过算法接口的load方法加载成为KNN分类器，使用findNearest方法进行预测。

OpenCV KNN预测方法API
    cv.ml.KNearest.findNearest(samples, k, results, neighborResponses, dist)
        - sample 待预测的数据样本
        - k 最近相邻的数目
        - result 预测结果
        - neighborResponse 每个样本的前k个邻居
        - dist 距离
"""


def main():
    # 加载KNN分类器
    knn = cv.ml.KNearest_load("knn_knowledge.yml")
    image = cv.imread("../../../raspberry-auto/pic/knn_01.png")
    cv.imshow("input", image)
    image = cv.resize(image, (20, 20))
    one = image.reshape(-1, 400)
    data = np.asarray(one).astype(np.float32)
    label = np.zeros((2, 1), dtype=np.float32)
    label[0][0] = 1
    _, result, neighbours, dist = knn.findNearest(data, k=5)
    for r in result:
        print(r[0])
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
