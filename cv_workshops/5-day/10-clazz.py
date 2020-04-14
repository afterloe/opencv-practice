#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
    矩形面积与弧长 
        通过计算轮廓的矩形与弧长，可以设定某个阈值实现ROI区域的过滤。
        
        轮廓点集的面积计算函数
        cv.contourArea(contour, oriented)
            - contour: 轮廓点集
            - oriented: boolean - default False， False -> 返回面积为正数； True -> 表示根据顺时针或逆时针返回正值或负值的面积
            
        轮廓点集的弧长计算函数
        cv.arcLength(curve, closed)
            - curve: 轮廓点集
            - closed: boolean， False -> 不闭合； True -> 闭合
"""


def main():
    """
        1 读取图像
        2 降燥
        3 灰度
        4 -> canny边缘提取
        5 -> 形态学操作
        4 连通组件搜寻
        5 矩形面积过滤
        6 连通组件最小面积绘制
        7 结果输出
    """
    src = cv.imread("../../pic/money.jpg")
    cv.namedWindow("src", cv.WINDOW_KEEPRATIO)
    cv.namedWindow("dst", cv.WINDOW_KEEPRATIO)
    cv.imshow("src", src)
    blur = cv.medianBlur(src, 71)
    t = 80
    canny_list = cv.Canny(blur, t, t * 2)
    k = np.ones((3, 3), dtype=np.uint8)
    binary = cv.morphologyEx(canny_list, cv.MORPH_DILATE, k)
    contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for index in range(len(contours)):
        contour = contours[index]
        area = cv.contourArea(contour)
        arc = cv.arcLength(contour, True)
        # 若面积小于 100 * 100 的像素区域 或 100的弧长
        if 10000 > area or 100 > arc:
            continue
        rect = cv.minAreaRect(contour)
        box = np.int0(cv.boxPoints(rect))  # int0 = int64
        cv.drawContours(src, [box], 0, (0, 0, 255), 2, cv.LINE_8)
        cx, cy = rect[0]
        cv.circle(src, (np.int32(cx), np.int32(cy)), 2, (255, 0, 0), 2, cv.LINE_8)
    cv.imshow("dst", src)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
