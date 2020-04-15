#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
基于KMeans的图像分割
    KMeans在opencv中用于图像分割，根据图像的各种像素值分割为几个指定类别颜色值，这种分割有2个具体的应用场景。其一是实现图像主色
彩的简单提取，另外一种就是对特定应用场景实现证件照片的背景替换的效果。
    对图像数据来说，需要在KMeans的图像进行数据处理，按行组织，相关函数使用reshape实现。
    
cv.Mat.reshape(cn, rows)
    - cn 图像通道数
    - rows 需要改多少行
"""

num_clusters = 2  # KMeans 集群的数, 即分成多少个类别


def main():
    image = cv.imread("../../../raspberry-auto/pic/Meter.jpg")
    # 图像按通道与BGR进行分割
    data = image.reshape(-1, 3)
    # 必须为浮点数的数据
    data = np.float32(data)
    # KMeans 分割条件
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, center = cv.kmeans(data, num_clusters, None, criteria, num_clusters, cv.KMEANS_RANDOM_CENTERS)
    # 图像转换为能够显示的类型
    center = np.uint8(center)
    # 使用中心的颜色值
    res = center[labels.flatten()]
    # 恢复图像通道
    dst = res.reshape(image.shape)
    cv.imshow("kmeans-image-demo", dst)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
