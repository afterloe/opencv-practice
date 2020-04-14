#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    自适应阈值算法：
        自适应阈值算法适合光照不均匀的图像进行阈值判断，通过均值模糊或 高斯模糊将图像进行光照均匀操作，再使用原图减去
    模糊的结果得到插值图像再进行自适应分割。
    
    cv.adaptiveThreshold(src, maxValue, adaptiveMethod, thresholdType, blockSize, C, dst)
        - maxValue: 二值化最大值
        - adaptiveMethod: 模糊方法 ADAPTIVE_THRESH_GAUSSIAN_C = 1 高斯; ADAPTIVE_THRESH_MEAN_C = 0 均值
        - thresholdType: 二值操作   THRESH_BINARY       二值图像 = 原图 – 均值图像 > -C ? 255 : 0
                                    THRESH_BINARY_INV   二值图像 = 原图 – 均值图像 > -C ? 0 : 255
        - blockSize: 卷积窗口（经验值: 25）,大的图像可以调整为127进行快速处理
        - C: 均匀阀值，不必设置太大，一般10、15左右
"""


def main():
    src = cv.imread("../../pic/document.jpg")
    cv.namedWindow("src", cv.WINDOW_AUTOSIZE)
    cv.namedWindow("binary", cv.WINDOW_AUTOSIZE)
    cv.imshow("src", src)
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    binary = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 25, 10)
    # _, binary = cv.threshold(gray, cv.mean(gray)[0], 255, cv.THRESH_BINARY)  # 光照不均匀的情况就容易丢失信息
    cv.imshow("binary", binary)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
