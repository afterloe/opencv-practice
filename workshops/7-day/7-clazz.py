#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    图像形态学操作 - 黑帽操作
        黑帽操作 = 闭操作 - 输入图像
        闭操作是先膨胀，再腐蚀，填充因为某些原因导致的像素断层，而黑帽操作在此基础上将结果减去原图像，可获得修复的结果。黑帽操作常用于工
    业上细小零件、组件的边缘提取与分析，使用morphologyEx进行操作，option枚举是`MORPH_BLACKHAT`
"""


def main():
    src = cv.imread("../../pic/dist_components.jpg")
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    blur = cv.medianBlur(gray, 3)
    _, binary = cv.threshold(blur, 0, 255, cv.THRESH_BINARY | cv.THRESH_TRIANGLE)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3), (-1, -1))
    dst = cv.morphologyEx(binary, cv.MORPH_BLACKHAT, kernel)
    cv.imshow("dst", dst)
    cv.imshow("binary", binary)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
