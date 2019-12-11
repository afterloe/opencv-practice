#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    opencv中的基本阈值操作：
        假设已有合适的阈值T，对其进行二值操作可以看成为一种阈值化操作。opencv中的阈值操作API如下。
        
        (double, dst) cv.threshold(src, dst, thresh, maxval, type)
            - thresh: 阈值
            - maxval: 像素二值操作最大值
            - type： 二值操作的方法
            
        type
            - THRESH_BINARY = 0         二值分割
            - THRESH_BINARY_INV = 1     反向二值分割
            - THRESH_TRUNC = 2          截断  (黑白图)
            - THRESH_TOZERO = 3         取零  (效果同0)
            - THRESH_TOZERO_INV = 4     反向取零
"""


def main():
    src = cv.imread("../../pic/luoxiaohei.jpg")
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    cv.imshow("src", src)
    T = cv.mean(gray)[0]
    for i in range(5):
        ret, binary = cv.threshold(gray, T, 255, i)
        cv.imshow("binary_" + str(i), binary)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
