#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
    工业品的缺陷检测
        工业品的缺陷检测是二值图像分析中的经典案例，分为两个部分进行，第一部分是通过图像分析提取指定的轮廓，第二部分是通过对比实现划痕检
    测与缺角检测。
        检测流程如下：
            输入图像 -> 二值化 -> 轮廓发现与分析 -> 轮廓排序 -> 填充/扩大 -> 模板比对 -> 结果输出
"""


def main():
    src = cv.imread("../../pic/blade.jpeg")
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3), (-1, -1))
    binary = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)
    contours, _ = cv.findContours(binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    height, width = src.shape[:2]
    for index in range(len(contours)):
        contour = contours[index]
        x, y, w, h = cv.boundingRect(contour)
        area = cv.contourArea(contour)
        if height // 2 < h or 150 > area:
            continue
        cv.rectangle(src, (x, y), (x + w, y + h), (255, 0, 0), 2, cv.LINE_8)
        cv.drawContours(src, contours, index, (0, 0, 255), 2, cv.LINE_8)
    cv.imshow("src", src)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
