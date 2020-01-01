#!/usr/bin/env
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
    自定义滤波器
        卷积最主要的的功能有 图像模糊、锐化、梯度边缘等，opencv允许通过不同的卷积实现自定义滤波操作，以下三个算子实现
    图像的均值
    
    1,1,1  0,-1,0    1,0
    1,1,1  -1,5,-1   0,-1
    1.1,1  0,-1,0
     模糊  锐化      梯度
        
    filter2D(src, ddepth, kernel, dst, anchor, delta, borderType)
        ddepth - 默认-1， 表示输入与输出图像类型一致，涉及浮点运算时，或卷积运算结果为负数时需要使用CV_32F；转换完成后
    使用convertScaleAbs函数将结果转换为字节类型
        kernel - 卷积 或 卷积窗口大小
        anchor - 中心像素点坐标
"""


def main():
    src = cv.imread("../../pic/money.jpg")
    cv.namedWindow("src", cv.WINDOW_AUTOSIZE)
    cv.imshow("src", src)
    blur_op = np.ones([5, 5], dtype=np.float32) / 25  # 均值模糊卷积
    shape_op = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)  # 锐化卷积
    grad_op = np.array([[1, 0], [0, -1]], dtype=np.float32)  # 梯度卷积

    dst = cv.filter2D(src, -1, blur_op)
    dst1 = cv.filter2D(src, -1, shape_op)
    dst2 = cv.filter2D(src, cv.CV_32F, grad_op)
    dst2 = cv.convertScaleAbs(dst2)  # 不转换，噪点太多
    cv.imshow("dst blur", dst)
    cv.imshow("dst shape", dst1)
    cv.imshow("dst grad", dst2)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
