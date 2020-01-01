#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
    图像形态学分析 - 开闭操作的结构元素切换应用演示
        在进行开闭操作时，根据结构元素的不同实现不同的二值图像处理效果，其中使提取二值图像中水平与垂直线比霍夫直线检测要好得多，本节为开
    闭操作的实践练习内容，并没有什么理论知识点。 
"""


def disk_recognition():
    """
        圆盘识别
    """
    src = cv.imread("../../pic/disk_recognition.jpg")
    blur = cv.GaussianBlur(src, (3, 3), 0)
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    binary = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 25, 10)
    # _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (55, 55))
    binary = cv.morphologyEx(binary, cv.MORPH_CLOSE, kernel)
    contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if 0 == len(contours):
        print("未发现 任何边缘")
        return
    for index in range(len(contours)):
        rect = cv.minAreaRect(contours[index])
        print(rect)
        cx, cy = rect[0]
        cv.circle(src, (np.int32(cx), np.int32(cy)), 1000, (255, 0, 0), 2, cv.LINE_8)
    cv.namedWindow("dst", cv.WINDOW_KEEPRATIO)
    cv.imshow("dst", src)


def completion_extract():
    """
        填空题 括号提取与标注

        1. 高斯降噪
        2. 灰度转换
        3. 二值化转换
        4. 开操作（选择直线形的结构元素，先腐蚀再膨胀， 将过于短小的直线去除，避免干扰）
        5. 二值图轮廓发现
        6. 绘制轮廓区域
    """
    # src = cv.imread("../../pic/test_paper.jpeg")  # 扫描仪获得的图片
    src = cv.imread("../../pic/test_paper.jpeg")  # 拍摄的照片
    blur = cv.GaussianBlur(src, (3, 3), 0)
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    # _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    # 由于拍摄的照片光照不均匀，使用自适应阈值更加合适
    binary = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 10)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (25, 1))  # 过滤阈值， 由于拍摄的照片中短线条偏多，故设置的小一点
    binary = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)
    contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if 0 == len(contours):
        print("未发现 任何边缘")
        return
    for index in range(len(contours)):
        x, y, w, h = cv.boundingRect(contours[index])  # 最大外接矩形
        y = y - 20
        h = 30
        cv.rectangle(src, (x, y), (x + w, y + h), (0, 0, 255), 1, cv.LINE_8)
    cv.imshow("dst", src)


def main():
    # completion_extract()
    disk_recognition()
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
