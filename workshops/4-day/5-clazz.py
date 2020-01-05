#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
   Unsharpen Mask 方法(USM) - 锐化增强算法
        (源图片 - w * 高斯模糊) / (1 - w) 
        * w -> 权重（0.1 ~ 0.9）, 默认为 0.6
        
    # 原理函数 - 图像融合函数（图像的shape、dtype一定要相同）
    cv.addWeighted(src1, alpha, src2, beta, gamma)
        - alpha: 第一个输入参数的权重值，可为负数
        - gamma: 类delta效果，色彩增强，总和超过255 就是白色
        - beta: 第二个输入参数的权重值，可为负数
"""


def main():
    # 1、 高斯模糊降噪
    # 2、 权重叠加
    src = cv.imread("../../pic/IMG_20191204_151110.jpg")
    cv.imshow("src", src)
    gauss = cv.GaussianBlur(src, (0, 0), 5)
    # media = cv.medianBlur(src, 5)  # 采用均值模糊（均值滤波）进行优化
    usm = cv.addWeighted(src, 1.5, gauss, -0.5, 0)
    cv.imshow("usm", usm)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
