#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
    Harris角点检测
        角点检测常用于工业仪表分析中提取指针、仪表的明显特征，对于一介倒数而言，角点在各方向的变化是最大的，而边缘区域只有在某一方向具有
    明显变化，后续的特征提取均布CNN替换，该示例仅作为示例进行。相关api描述如下：
        cv.cornerHarris(gary, blockSize, aperture_size, k)
            - gray: 单通道图像，可以是float、int32、int0等
            - blockSize: 计算方差矩阵的相邻域像素大小
            - aperture_size: soble算子大小(梯度算法 的卷积核)
            - k: 表示系数，经验值 0.04 ~ 0.06
"""


def process(image):
    dst = image
    block_size = 2
    aperture_size = 3
    k = 0.04
    gray = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)
    # 角点检测
    dst = cv.cornerHarris(gray, block_size, aperture_size, k)
    dst_normal = np.empty(dst.shape, dst.dtype)
    # 角点检测的结果进行 归一化处理
    dst_normal = cv.normalize(dst, dst_normal, alpha=0, beta=255, norm_type=cv.NORM_MINMAX)
    for i in range(dst_normal.shape[0]):
        for j in range(dst_normal.shape[1]):
            if int(dst_normal[i, j]) > 80:
                b = np.random.randint(0, 256)
                g = np.random.randint(0, 256)
                r = np.random.randint(0, 256)
                cv.circle(image, (j, i), 5, (int(b), int(g), int(r)), 2)
    return image


def main():
    src = cv.imread("../../../raspberry-auto/pic/ele_panel.jpg")
    cv.imshow("src", src)
    result = process(src)
    cv.imshow("dst", result)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
