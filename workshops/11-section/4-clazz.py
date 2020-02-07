#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
KNN算法简介

    OpenCV中机器学习模块的最近邻算法KNN， 使用KNN算法实现手写数字识别
    
大致的顺序如下：
1.	读入测试图像digit.png(OpenCV在sample/data中有一张自带的手写数字数据集图像，0~9 每个有500个样本，总计有5000个数字)
2.	构建样本数据与标签
3.	创建KNN训练并保存训练结果

图像大小为1000x2000的大小图像，分割为20x20大小的单个数字图像，每个样本400个像素。然后使用KNN相关API实现训练与结果的保存。
"""


def main():
    # 这张图是opencv中的手写体集合
    image = cv.imread("../../../raspberry-auto/pic/digits.png")
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # 对图片进行分割， 50行，每行100 列
    cells = [np.hsplit(row, 100) for row in np.vsplit(gray, 50)]
    x = np.array(cells)
    # 将前50个列为训练素材
    train = x[:, : 50].reshape(-1, 400).astype(np.float32)
    # 将后50个作为测试素材
    test = x[:, 50: 100].reshape(-1, 400).astype(np.float32)
    k = np.arange(10)
    # 编写对应的标签
    train_labels = np.repeat(k, 250)[:, np.newaxis]
    test_labels = train_labels.copy()
    # 创建knn
    knn = cv.ml.KNearest_create()
    # 训练
    knn.train(train, cv.ml.ROW_SAMPLE, train_labels)
    # 识别
    _, result, neighbours, dist = knn.findNearest(test, k=5)
    # 计算准确率
    matches = result == test_labels
    correct = np.count_nonzero(matches)
    accuracy = correct * 100.0 / result.size
    print(accuracy)  # 输出准确率 91.76
    knn.save("knn_knowledge.yml")  # 保存样本


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
