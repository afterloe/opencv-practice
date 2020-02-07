#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
决策树算法
    opencv中机器学习模块的决策树算法分为两个类别，一个是随机森林，另一个强化分类，这两种算法都属于决策树算法，相关api如下

cv.ml.StatModel.predict(samples, results, flags)
    - sample 输入样本
    - results 预测结果
"""


def main():
    image = cv.imread("../../../raspberry-auto/pic/digits.png")
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    cells = [np.hsplit(row, 100) for row in np.vsplit(gray, 50)]
    x = np.array(cells)
    train = x[:, : 50].reshape(-1, 400).astype(np.float32)
    test = x[:, 50: 100].reshape(-1, 400).astype(np.float32)
    k = np.arange(10)
    train_labels = np.repeat(k, 250)[:, np.newaxis]
    test_labels = train_labels.copy()
    dt = cv.ml.RTrees_create()
    # 训练
    dt.train(train, cv.ml.ROW_SAMPLE, train_labels)

    # 预测
    _, results = dt.predict(test)

    # 计算准确率
    matches = results == test_labels
    correct = np.count_nonzero(matches)
    accuracy = correct * 100.0 / results.size
    print(accuracy)  # 输出准确率 83.72


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
