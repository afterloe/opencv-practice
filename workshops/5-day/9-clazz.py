#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
    轮廓外接矩形：
        轮廓外接矩形分为最大外接矩形与最小外接矩形两种，使用这种方法可以将物体的轮廓剪切下来并发送到对应的识别软件进行处理。不过需要注意
    的在使用外接矩形的时候不推荐进行二值化操作，因为容易将深颜色的物体过滤掉。具体api如下：
    
        外接矩形API
        rect = cv.boundingRect(gray)
            - gray: 灰度图像或2D点阵数组
            - rect: 返回矩形轮廓x, y, w, h
            
        最小外接矩形
        angle, center, size = cv.minAreaRect(points)
            - points: 点整集
"""


def main():
    src = cv.imread("../../pic/money.jpg")
    src_copy = src.copy()
    cv.namedWindow("src", cv.WINDOW_KEEPRATIO)
    cv.namedWindow("dst - boundingRect", cv.WINDOW_KEEPRATIO)
    cv.namedWindow("dst - minAreaRect", cv.WINDOW_KEEPRATIO)
    cv.imshow("src", src)
    blur = cv.medianBlur(src, 15)
    t = 80
    binary = cv.Canny(blur, t, t * 2)
    k = np.ones((3, 3), dtype=np.uint8)
    binary = cv.morphologyEx(binary, cv.MORPH_DILATE, k)  # cv形态学操作
    contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # 绘制 最大矩形
    for index in range(len(contours)):
        x, y, w, h = cv.boundingRect(contours[index])
        cv.rectangle(src, (x, y), (x + w, y + h), (0, 0, 255), 1, cv.LINE_8)
        rect = cv.minAreaRect(contours[index])
        cx, cy = rect[0]  # 中心点坐标
        box = cv.boxPoints(rect)  # opencv 中的api， 快速绘制带有角度的矩形
        box = np.int32(box)  # 将结果转换为int32 类型
        cv.drawContours(src_copy, [box], 0, (0, 0, 255), 2, cv.LINE_8)
        cv.circle(src_copy, (np.int32(cx), np.int32(cy)), 2, (255, 0, 0), 2, cv.LINE_8)
    cv.imshow("dst - boundingRect", src)
    cv.imshow("dst - minAreaRect", src_copy)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
