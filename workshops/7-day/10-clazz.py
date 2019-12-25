#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    形态学操作 - hit&miss操作
        hit&miss操作指的是结构元素对二值图像进行过滤，若领域内的图像符合结构元素描述则保留，若不符合结构元素描述则过滤，可以用于断面检
    测，组件连通状态检测等内容，同样使用morphologyEx进行，option为 `MORPH_HITMISS`
"""


def main():
    src = cv.imread("../../pic/net.png")
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    blur = cv.medianBlur(gray, 3)
    _, binary = cv.threshold(blur, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    cv.imshow("binary", binary)
    kernel = cv.getStructuringElement(cv.MORPH_CROSS, (11, 11))  # 十字交叉 结构元素
    binary = cv.morphologyEx(binary, cv.MORPH_HITMISS, kernel)
    cv.imshow("dst", binary)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
