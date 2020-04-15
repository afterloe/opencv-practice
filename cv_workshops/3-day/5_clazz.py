#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    图像去噪在ocr、机器人视觉及机器视觉有至关重要，对图像二值化与二值分析很有帮助，常用的去噪方式有：
        - 均值去噪
        - 高斯模糊去噪
        - 非局部均值去噪
        - 双边滤波去噪
        - 形态学去噪
    3 * 3 的去噪足够， 不行就 5 * 5 ， 卷积太大会导致图像丢失内容
    
    dnoise max 15，最好不超过10， opencv默认为3
    窗口大小推荐为 1： 3 即 搜索窗口为 卷积的3倍
"""


def main():
    src = cv.imread("G:/Project/raspberry-auto/pic/gaussian_noise.png")
    cv.namedWindow("input", cv.WINDOW_AUTOSIZE)
    cv.imshow("input", src)
    ksize = (3, 3)
    result1 = cv.blur(src, ksize)
    result2 = cv.GaussianBlur(src, ksize, 0)
    result3 = cv.medianBlur(src, 3)
    result4 = cv.fastNlMeansDenoisingColored(src, None, 15, 15, 10, 30)  # 磨皮效果
    cv.imshow("blur", result1)
    cv.imshow("gaussian blur", result2)
    cv.imshow("median blur", result3)
    cv.imshow("fast nl means", result4)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
