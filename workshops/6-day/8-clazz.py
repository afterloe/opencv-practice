#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
    霍夫直线检测二:
        其实opencv中还有一个霍夫直线的检测api，该api更为常用，它会直接返回直线的空间坐标点，比之前点阵集合更加直观，更容易理解。同时该
    api能够声明最短线段长度、中间缺省线段等。而前一课的api适用于多个备选线段并进行一系列算法使用，两种api均有自己的使用场景。
    
    cv.HoughLinesP(binary, rho, theta, threshold, minLineLength, maxLineGap)
        - binary: 具有轮廓的二值图
        - rho: 极坐标 r的步长  经验值：1
        - theta: 角度的步长 经验值: np.pi / 180
        - threshold: 累加器阈值,图像在霍夫空间每个像素点都是一条曲线，经过的每个(r,theta)都加1，如果多个曲线都经过同一个
    (r,theta)相交，如果大于给定的域值，说明可能存在一条直线在霍夫空间该点
        - minLineLength: 最小线段长度
        - maxLineGap: 最大线段终端像素    
"""


def main():
    src = cv.imread("../../pic/sw/sw_sale_drug.png")
    T = 80
    blur = cv.medianBlur(src, 15)
    binary = cv.Canny(blur, T, T * 2)
    # minLineLength的值与threshold的相差不多，一般相等
    linesP = cv.HoughLinesP(binary, 1, np.pi / 180, 50, None, 50, 10)
    if None is linesP:
        print("can't find line")
        return
    dist = np.zeros(src.shape, dtype=np.uint8) * 255
    for index in range(len(linesP)):
        line = linesP[index][0]  # 检测到的直线信息
        cv.line(dist, (line[0], line[1]), (line[2], line[3]), (255, 0, 0), 1, cv.LINE_AA)
    cv.imshow("dist", dist)
    cv.imshow("src", src)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
