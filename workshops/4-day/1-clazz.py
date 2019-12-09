#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    Sobel算子:
        卷积的作用除了实现图像模糊、降噪外，还可实现梯度信息寻找。这类梯度信息是图像的原始特征数据，进行一步处理后可生
    成一些比较高级的特征，可用于图像特征的匹配、图像分类等应用，Sobel算子是一种很典型的图像梯度提取算子，其本质是基于
    图像空间域卷积，实现思想为一阶导数算子。
    
    cv.Sobel(src, ddepth, dx, dy, ksize, scale, delta, borderType)
        ddepth - 表示输入与输出图像类型关系, CV_32F；若为 -1 则会出现不可预期的结果
        dx - X方向 一阶导数
        dy - Y方向 一阶导数
        ksize - 卷积大小 3*3
        scale - 缩放比率， 1表示不变
        borderType - 边缘类型
"""


def main():
    src = cv.imread("../../pic/IMG_20191204_151110.jpg")
    cv.imshow("src", src)
    h, w = src.shape[:2]
    x_grad = cv.Sobel(src, cv.CV_32F, 1, 0)  # X方向求导
    y_grad = cv.Sobel(src, cv.CV_32F, 0, 1)  # Y方向求导

    x_grad = cv.convertScaleAbs(x_grad)
    y_grad = cv.convertScaleAbs(y_grad)    # 结果转换，将32位转换为 8位，实现结果展示
    # cv.imshow("x_grad", x_grad)
    # cv.imshow("y_grad", y_grad)

    dst = cv.add(x_grad, y_grad, dtype=cv.CV_16S)  # 32位相加，取值范围为0 ~ 512
    dst = cv.convertScaleAbs(dst)  # 结果转换
    cv.imshow("gradient", dst)

    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()

