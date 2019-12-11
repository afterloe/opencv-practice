#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
        图像卷积的主要三个功能为 图像模糊 -> 去噪、 图像梯度 -> 边缘发现、 图像锐化 -> 细节增强。图像锐化的本质是图像
    拉普拉斯滤波器加原图权重像素叠加输出的结果。同样使用自定义滤波器带入对应算子实现
    
    -1 -1 -1
    -1  C -1     --->  当C大于8时，表示图像锐化，越接近8表示锐化效果越好; 等于8时是图像高通滤波()；
    -1 -1 -1
        8领域
        
    0 -1 0
    -1 5 -1
    0 -1 0
        4领域
"""


def main():
    src = cv.imread("../../pic/IMG_20191204_151110.jpg")
    cv.imshow("src", src)
    sharp_kernel = np.asarray([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)  # 4领域锐化
    # sharp_kernel = np.asarray([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]], dtype=np.float32)  # 8领域锐化, 效果强烈`
    dst = cv.filter2D(src, cv.CV_32F, kernel=sharp_kernel)
    dst = cv.convertScaleAbs(dst)
    cv.imshow("dst", dst)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
