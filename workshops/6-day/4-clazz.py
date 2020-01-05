#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
  轮廓拟合 - 圆，椭圆
    轮廓拟合用于解决二值图像分析过程中，多轮廓缺省或其他原因导致的图像不闭合的问题，通过对轮廓进行进一步处理，满足对轮廓形状的判断。
    cv.fitEllipse(contours)
        - contours: 轮廓
    
    return:
        - 拟合后的中心位置
        - 长轴与短轴的直径（如果是圆，则两个值相同）
        - 偏移角度
    
    注意： contours进行椭圆拟合操作时最少需要5个点
"""


T = 80


def main():
    src = cv.imread("../../pic/hw_freebuds3_2.jpg")
    cv.namedWindow("dst", cv.WINDOW_KEEPRATIO)
    blur = cv.medianBlur(src, 17)
    canny_list = cv.Canny(blur, T, T * 2)
    k = np.ones((3, 3), dtype=np.uint8)
    binary = cv.morphologyEx(canny_list, cv.MORPH_DILATE, k)
    contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for index in range(len(contours)):
        # 若 轮廓小于5个点， 表示为其他形状，不进行拟合操作
        if 5 >= len(contours[index]):
            continue
        (cx, cy), (a, b), angle = cv.fitEllipse(contours[index])
        cv.ellipse(src, (np.int32(cx), np.int32(cy)),
                   (np.int32(a / 2), np.int32(b / 2)), angle, 0, 360, (0, 0, 255), 2, cv.LINE_8)

    cv.imshow("dst", src)
    cv.waitKey(0)
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
