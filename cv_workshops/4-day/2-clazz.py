#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
    图像梯度 - 自定义梯度算子
        对于一阶求导用Sobel算子外，还有robert和prewitt算子， 这两了算子可使用Opencv中的自定义滤波器实现。其中
        ddepth 不推荐继续使用-1了，因为其表示输入与输出图像类型关系，涉及浮点运算时，或卷积运算结果为负数时需要使用CV_32F
    或np.float32；转换完成后使用convertScaleAbs函数将结果转换为字节类型
    
    robert卷积核如下:
    1, 0      0, -1
    0, -1     1, 0
    x方向      y方向
    
    prewitt卷积核如下:
    -1, -1, -1       -1, 0, 1
    0, 0, 0          -1, 0, 1
    1, 1, 1          -1, 0, 1
    x方向              y方向
"""


def prewitt_calculation(src):
    prewitt_y = np.asarray([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
    dst = cv.filter2D(src, cv.CV_16S, prewitt_y)
    dst = cv.convertScaleAbs(dst)
    cv.imshow("prewitt_y", dst)


def robert_calculation(src):
    robert_x = cv.filter2D(src, cv.CV_16S, np.asarray([[1, 0], [0, -1]], dtype=np.float32))
    robert_x = cv.convertScaleAbs(robert_x)
    cv.imshow("robert_x", robert_x)


def main():
    src = cv.imread("../../pic/IMG_20191204_151110.jpg")
    cv.imshow("src", src)
    prewitt_calculation(src)
    robert_calculation(src)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
