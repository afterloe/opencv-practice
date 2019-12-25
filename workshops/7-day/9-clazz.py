#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    形态学分析应用 - 使用基本梯度对轮廓进行分析处理
        使用形态学的二值化处理，对是别内容进行轮廓分析，在OCR上是其处理的手段之一，相比于threshold的二值化而言，对图像会有更好的分割效
    果，技术路线如下:
        1 图像形态学梯度
        2 灰度
        3 全局阈值二值化
        4 轮廓分析
"""


def main():
    src = cv.imread("../../pic/1.jpg")
    blur = cv.medianBlur(src, 3)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    gradient = cv.morphologyEx(blur, cv.MORPH_GRADIENT, kernel)
    cv.imshow("gradient", gradient)
    gray = cv.cvtColor(gradient, cv.COLOR_BGR2GRAY)
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    cv.imshow("binary", binary)
    # binary = cv.morphologyEx(binary, cv.MORPH_DILATE, cv.getStructuringElement(cv.MORPH_CROSS, (3, 3)))  # 膨胀 3*3 十字交叉
    contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if 0 == len(contours):
        print("未搜寻到结果")
        return
    for index in range(len(contours)):
        contour = contours[index]
        x, y, w, h = cv.boundingRect(contour)  # 获取最大外接矩形
        area = cv.contourArea(contour)  # 获取轮廓面积
        if not 10 < area < 500 or not 10 < h < 60:
            continue
        cv.rectangle(src, (x, y), (x + w, y + h), (0, 0, 255), 2, cv.LINE_8)
    cv.imshow("src", src)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
