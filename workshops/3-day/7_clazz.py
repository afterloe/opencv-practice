#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    边缘保留滤波算法 - 均值迁移模糊
        均值迁移模糊常用于分水岭分割前去噪，提升分割效果。主要思想是在卷积操作时对卷积中的像素值空间符合分布的像素点
    参与计算，获得像素均值与空间位置均值，使用新的均值位置作为窗口中心继续基于给定的像素值空间分布迁移，如此不断的迁移
    直到不再移动。
    
    pyrMeanShiftFiltering(src, sp, sr, dst, maxLevel, termCriteria)
        sp - 卷积窗口的大小(半径)
        sr - 卷积窗口的颜色范围，即参与运算的像素数量
        maxLevel - default: 1
        termCriteria - 停止条件
"""


def main():
    src = cv.imread("../../pic/IMG_20191204_151110.jpg")
    cv.namedWindow("src", cv.WINDOW_AUTOSIZE)
    cv.imshow("src", src)
    dst = cv.pyrMeanShiftFiltering(src, 15, 30, termcrit=(
        cv.TERM_CRITERIA_MAX_ITER + cv.TERM_CRITERIA_EPS,
        5, 1  # 5 次，若增加次数，会增强运算时间
    ))
    cv.imshow("dst", dst)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
