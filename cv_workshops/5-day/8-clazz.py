#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
    轮廓发现
        通过图像连通组件的分析后获取基于二值图像的每个连通组件，通过对应的点连接获取各组件的之间的层次关系与几何拓扑关系，使用opencv的
    api 以发现连通组件间的轮廓。
        contours, hierarchy	= cv.findContours(binary, mode, method[, contours[, hierarchy[, offset]]]) 
            in
            - binary: 二值图
            - mode: 轮廓寻早的拓扑结构返回模式，RETR_EXTERNAL 只返回最外层轮廓；RETR_TREE 返回轮廓树结构
            - method: 轮廓点吉和算法，常见的是基于CHAIN_APPROX_SIMPLE链式编码方法
            - offset: 表示偏移缩放量
            out
            - contours: 轮廓点集合
            - hierarchy: 每个轮廓的四个相关信息，分别是同层下一个轮廓索引、同层上一个轮廓索引、下层第一个子索引、上层父轮廓索引
            
        opencv中绘制轮廓的api
        image =	cv.drawContours(dst, contours, contourIdx, color[, thickness[, lineType[, hierarchy[, maxLevel[, offset]]]]])
            - dst: 绘制的底图, 目标图像
            - contours: 轮廓集
            - contourIdx: > 0 绘制该轮廓， -1 绘制子所有轮廓
            - thickness: 轮廓线厚度，> 0 绘制轮廓， < 0 填充
"""


def threshold_image(image):
    blur = cv.medianBlur(image, 5)
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    cv.imshow("binary", binary)
    return binary


def main():
    src = cv.imread("../../pic/money.jpg")
    binary = threshold_image(src)
    contours, hierarchy = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    dst = np.zeros(src.shape, dtype=src.dtype)
    for contour in range(len(contours)):
        cv.drawContours(dst, contours, contour, (0, 0, 255), 2, cv.LINE_8)
    cv.imshow("dst", dst)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
