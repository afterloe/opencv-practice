#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    形态学操作 - 顶帽操作
        顶帽操作 = 原图 - 开操作
        用于提取图像中细微的部分，由于开操作是先腐蚀，再膨胀，去除了细微部分的变化，使用原图减去开操作的结果，可以获得被去除了的细微部分
    的像素，同样使用 morphologyEx进行操作，option枚举为 `MORPH_TOPHAT`
"""


def main():
    src = cv.imread("../../pic/1yuan.jpg")
    blur = cv.medianBlur(src, 15)
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (9, 9), (-1, -1))
    dst = cv.morphologyEx(binary, cv.MORPH_TOPHAT, kernel)
    cv.namedWindow("dst", cv.WINDOW_KEEPRATIO)
    cv.imshow("dst", dst)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
