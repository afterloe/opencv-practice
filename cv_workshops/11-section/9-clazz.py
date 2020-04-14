#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
Grabcut图像分割实现背景替换
    使用Grabcut实现图像对象提取，通过背景图像替换，实现图像合成，通过对背景图像高斯模糊实现背景虚化效果，完整步骤如下:
    
1 ROI区域选择
2 Gradbcut对象分割
3 Mask生成
4 使用Mask实现背景与前景的高斯权重融合
"""


def main():
    image = cv.imread("../../../raspberry-auto/pic/49a1f637jw1evzjx6ljr6j213l1gshdt.jpg")
    background = cv.imread("../../../raspberry-auto/pic/3.png")
    mask = np.zeros(image.shape[: 2], dtype=np.uint8)
    rect = cv.selectROI("select roi", image)
    h, w, ch = image.shape
    bgd_model = np.zeros((1, 65), np.float64)  # 65 = 13 * 5
    fgd_model = np.zeros((1, 65), np.float64)  # 这里的值必须是 13的整数倍， 最右值为iterCount * 13
    cv.grabCut(image, mask, rect, bgd_model, fgd_model, 5, mode=cv.GC_INIT_WITH_RECT)
    mask2 = np.where((1 == mask) + (3 == mask), 255, 0).astype("uint8")
    print(mask2.shape)
    se = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    cv.dilate(mask2, se, mask2)
    mask2 = cv.GaussianBlur(mask2, (5, 5), 0)
    cv.imshow("background-mask", mask2)
    background = cv.GaussianBlur(background, (0, 0), 15)
    result = np.zeros((h, w, ch), dtype=np.uint8)
    for row in range(h):
        for col in range(w):
            w1 = mask2[row, col] / 255.0
            b, g, r = image[row, col]
            b1, g1, r1 = background[row, col]
            b = (1.0 - w1) * b1 + b * w1
            g = (1.0 - w1) * g1 + g * w1
            r = (1.0 - w1) * r1 + r * w1
            result[row, col] = (b, g, r)
    cv.imshow("result", result)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
