#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
Grabcut图像分割

    Grabcut是基于图割(graph cut)实现的图像分割算法，它需要用户输入一个bounding box作为分割目标位置，实现对目标与背景的分离/
分割，因此在很多APP图像分割/背景虚化的软件中可以看到其身影。相关API如下：

cv.grabCut(img, mask, rect, bgdModel, fgdModel, iterCount, mode)
    - img 输入的三通道图像
    - mask 输入的单通道图像，初始化方式为GC_INIT_WITH_RECT 表示ROI区域可以被初始化为
        GC_BGD 定义为明显的背景像素 0
        GC_FGD 定义为明显的前景像素 1
        GC_PR_BGD 定义为可能的背景像素 2
        GC_PR_FGD 定义为可能的前景像素 3
    - rect ROI区域
    - bgdModel 临时背景模型数组
    - fgdModel 临时前景模型数组
    - iterCount 图割算法迭代次数
    - mode 当使用用户提供的roi时候使用GC_INIT_WITH_RECT
"""


def main():
    image = cv.imread("../../../raspberry-auto/pic/49a1f637jw1evzjx6ljr6j213l1gshdt.jpg")
    cv.imshow("src", image)
    mask = np.zeros(image.shape[: 2], dtype=np.uint8)
    rect = cv.selectROI("select", image)
    print(rect)
    bgd_model = np.zeros((1, 65), np.float64)  # 65 = 13 * 5
    fgd_model = np.zeros((1, 65), np.float64)  # 这里的值必须是 13的整数倍， 最右值为iterCount * 13
    cv.grabCut(image, mask, rect, bgd_model, fgd_model, 5, mode=cv.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 1) + (mask == 3), 255, 0).astype('uint8')
    print(mask2.shape)
    result = cv.bitwise_and(image, image, mask=mask2)
    cv.imshow("dst", result)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
