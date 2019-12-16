#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
    轮廓逼近
        对图像的二值图各轮廓进行相似操作，逼近每个林廓的真实几何形状，从而通过轮廓判断真实物品是什么形状， 但该种判断十分脆弱，后续会有
    更好的算法来实现该功能
    
    cv.approxPolyDP(cure, approxCurve, epsilon, closed)
        - curve: 轮廓曲线点
        - approxCurve: 输出的顶点数目
        - epsilon: 真实曲线的最大距离，值越小越逼近真实轮廓
        - closed: 区域是否闭合
"""


def judge(contour):
    result = cv.approxPolyDP(contour, 4, True)
    vertexes = result.shape[0]
    print(vertexes)
    if 3 is vertexes:
        print("三角形")
    if 4 is vertexes:
        print("矩形")
    if 6 is vertexes:
        print("六边形")
    if 10 < vertexes:
        print("圆形")


def main():
    src = cv.imread("../../pic/huawei_freebuds3.jpg")
    cv.namedWindow("src", cv.WINDOW_KEEPRATIO)
    cv.namedWindow("dst", cv.WINDOW_KEEPRATIO)
    cv.imshow("src", src)
    blur = cv.medianBlur(src, 15)
    binary = cv.Canny(blur, 80, 160)
    k = np.ones((3, 3), dtype=np.uint8)
    binary = cv.morphologyEx(binary, cv.MORPH_DILATE, k)
    contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for index in range(len(contours)):
        contour = contours[index]
        area = cv.contourArea(contour)
        if 100 > area:
            continue
        rect = cv.minAreaRect(contour)
        box = np.int0(cv.boxPoints(rect))
        cv.drawContours(src, [box], 0, (255, 0, 0), 2, cv.LINE_8)
        judge(contour)

    cv.imshow("dst", src)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
