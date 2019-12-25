#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    图像形态学操作 - 闭操作
        闭操作 = 膨胀 + 腐蚀
        与开操作的相对应的是闭操作，闭操作是先膨胀，再腐蚀，用于填充图像中缺少的二值区域即中心孔洞填充，形成完整的闭合区域连通组件，使用
    同样的api进行操作，闭操作的option枚举是 MORPH_CLOSE
"""


def main():
    src = cv.imread("../../pic/money.jpg")
    cv.namedWindow("dst", cv.WINDOW_KEEPRATIO)
    cv.namedWindow("binary", cv.WINDOW_KEEPRATIO)
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (35, 35), 0)
    _, binary = cv.threshold(blur, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (25, 25))
    dst = cv.morphologyEx(binary, cv.MORPH_CLOSE, kernel)
    cv.imshow("dst", dst)
    cv.imshow("binary", binary)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
