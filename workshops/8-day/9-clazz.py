#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
    视频分析 - 背景消除与前景ROI提取
        通过视频中的背景进行建模（GMM、KNN等）实现背景消除，生成mask图像，通过对mask二值图像分析实现对前景活动对象ROI区域的提取，也是
    很多视频监控分析软件常用的手段，其工作原理如下：
        1 初始化背景建模对象
        2 读取视屏
        3 使用背景建模消除生成mask
        4 对mask进行轮廓分析提取ROI
        5 绘制ROI对象
"""


def process(frame, model):
    mask = model.apply(frame)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 5), (-1, -1))
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for index in range(len(contours)):
        contour = contours[index]
        area = cv.contourArea(contour)
        if 350 > area:
            continue
        rect = cv.minAreaRect(contour)
        cv.ellipse(frame, rect, (255, 0, 0), 2, cv.LINE_8)
        cv.circle(frame, (np.int32(rect[0][0]), np.int32(rect[0][1])), 2, (0, 0, 255), 2, cv.LINE_8)
    return frame


def main():
    avi = "../../pic/vtest.avi"
    capture = cv.VideoCapture(avi)
    bs_knn = cv.createBackgroundSubtractorKNN(history=500, dist2Threshold=100, detectShadows=False)
    while True:
        ret, frame = capture.read()
        if True is not ret:
            print("can't read any video!")
            break
        dst = process(frame, bs_knn)
        cv.imshow("dst", dst)
        key = cv.waitKey(10) & 0xFF
        if 27 == key:  # ESC
            break
    capture.release()
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
