#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import imutils
from imutils.perspective import four_point_transform
import numpy as np
import os

"""
步骤1：检测边缘。
步骤2：使用图像中的边缘来查找表示被扫描纸张的轮廓（轮廓）。
步骤3：应用透视图转换以获取文档的自顶向下视图。
"""

STEP = 500


class ScanRunner(object):

    def __init__(self, image):
        if False is os.path.isfile(image):
            assert Exception("%s 图像不存在" % image)
        self.__image = cv.imread(image)

    def run(self):
        h, w = self.__image.shape[: 2]
        ratio = h / float(STEP)
        image = imutils.resize(self.__image, height=STEP)
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        # 双边滤波, 一种非线性的滤波方法，是结合图像的空间邻近度和像素值相似度的一种折衷处, 达到保边去噪的目的
        """
        cv::bilateralFilter(
            InputArray src,
            int 	d,
            double 	sigmaColor,
            double 	sigmaSpace,
            int 	borderType = BORDER_DEFAULT 
        )
        int d: 表示在过滤过程中每个像素邻域的直径范围。如果这个值是非正数，则函数会从第五个参数sigmaSpace计算该值。 
        double sigmaColor: 颜色空间过滤器的sigma值，这个参数的值越大，表明该像素邻域内有越宽广的颜色会被混合到一起，产生较大的半相等颜色区域。
         double sigmaSpace: 坐标空间中滤波器的sigma值，如果该值较大，则意味着越远的像素将相互影响，从而使更大的区域中足够相似的颜色获取相同的颜色。
         int borderType=BORDER_DEFAULT: 用于推断图像外部像素的某种边界模式
        """
        blurred = cv.bilateralFilter(gray, 5, 17, 17)
        # blurred = cv.GaussianBlur(gray, (5, 5), 0)
        edged = cv.Canny(blurred, 75, 200)
        cv.imshow("image", image)
        cv.imshow("edged", edged)
        cv.namedWindow("output", cv.WINDOW_FREERATIO)
        cv.namedWindow("thresh", cv.WINDOW_FREERATIO)

        cnts = cv.findContours(edged, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv.contourArea, reverse=True)[: 5]
        screen_cnt = None
        for c in cnts:
            # 这种算法通常被称为Ramer - Douglas - Peucker算法，或者简单地称为分割合并算法。
            # 计算周长
            peri = cv.arcLength(c, True)
            # cv2.approxPolyDP的第二个参数的值通常在原始轮廓周长的1 - 5 % 范围内。
            approx = cv.approxPolyDP(c, 0.02 * peri, True)
            if 4 == len(approx):
                screen_cnt = approx
                break
        cv.drawContours(image, [screen_cnt], -1, (0, 255, 255), 2)
        cv.imshow("outline", image)

        warped = four_point_transform(self.__image, screen_cnt.reshape(4, 2) * ratio)
        cv.imshow("output", warped)
        # warped = cv.GaussianBlur(warped, (15, 15), 0)
        warped = cv.cvtColor(warped, cv.COLOR_BGR2GRAY)
        
        value, thresh = cv.threshold(warped, 255, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
        # 自适应阈值， 后两个参数 - 卷积核 大小，越大越快； 均匀阀值，不必设置太大，一般10、15左右
        # thresh = cv.adaptiveThreshold(warped, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 45, 10)
        outs = (warped > value).astype("uint8") * 255
        cv.imshow("outs", outs)

        cv.imshow("thresh", thresh)

        cv.waitKey(0)
        pass
