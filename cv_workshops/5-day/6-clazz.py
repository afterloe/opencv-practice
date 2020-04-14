#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import imutils
import numpy as np

"""
    连通组件寻找
        连通组件标记算法是图像分析中最常用的算法之一， 原理是扫描二值图像的每个像素点，对于像素值相同且相互连通的分为一个组，最终得到图像
    中所有的像素连通组件。扫描的方式是从上到下，从左到右。最大联通组件个数为N/2，其中N表示图像的总像素个数；该算法在调用时，必须保证背景
    像素是黑色，前景像素是白色。最常见的连通组件扫描的有以下两类：
        - 一步法： 基于图的搜索算法
        - 两步法： 基于扫描与等价类合并算法
        
    cv.connectedComponents(binary, labels, connectivity, ltype)
        - binary: 输入二值图像， 黑色背景
        - labels: 输出的标记图像，背景index为0
        - connectivity: 连通域， 如8领域、4领域； 默认是8领域
        - ltype: 输出的labels类型，默认是CV_32S
"""


def main():
    src = cv.imread("../../pic/money.jpg")
    # 均值模糊， ksize越大，越模糊
    blur = cv.blur(src, (55, 55))
    # 转换为 灰度图像
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    # 对灰度图像进行 二值化，使用OTSU 算法进行
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    # 连通组件标记算法
    output = cv.connectedComponents(binary, connectivity=8, ltype=cv.CV_32S)
    num_labels = output[0]  # 获取组件的数量
    labels = output[1]  # 获取组件
    # 为每个组件设置随机颜色
    colors = []
    for i in range(num_labels):
        b = np.random.randint(0, 256)
        g = np.random.randint(0, 256)
        r = np.random.randint(0, 256)
        colors.append((b, g, r))
    colors[0] = (0, 0, 0)  # 背景设置为 黑色
    h, w = gray.shape
    # 结果输出
    image = np.zeros((h, w, 3), dtype=np.uint8)
    for row in range(h):
        for col in range(w):
            image[row, col] = colors[labels[row, col]]
    src = imutils.resize(src, 640, 320)
    image = imutils.resize(image, 640, 320)
    cv.imshow("result", image)
    cv.imshow("src", src)
    # 组件数量， 减一表示去除背景
    print("total money is %d " % (num_labels - 1))
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
