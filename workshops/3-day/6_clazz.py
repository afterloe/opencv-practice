#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    边缘保留滤波算法 - 高斯双边模糊
        该算法为ps磨皮算法的底层算法，也是美图软件使用的算法，边缘保留滤波算法可以在模糊过程中保存图像
    完整轮廓，常用算法有以下几种：
        - 高斯双边
        - Meanshift均值迁移
        - 局部方差模糊
        - opencv专门API
        
"""


def main():
    src = cv.imread("G:/Project/raspberry-auto/pic/5yuan.jpg")
    cv.namedWindow("input", cv.WINDOW_AUTOSIZE)
    cv.imshow("input", src)
    # 高斯双边模糊
    # d - 浮动值，缩放比列，一般设置为0
    # sigmaColor - 像素色差，即参与模糊运算的像素阈值
    dst = cv.bilateralFilter(src, 0, 100, 10)
    cv.imshow("output", dst)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
