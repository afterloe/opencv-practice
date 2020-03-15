#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import imutils
from imutils.perspective import four_point_transform
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
        blurred = cv.GaussianBlur(gray, (5, 5), 0)
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
            peri = cv.arcLength(c, True)
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
        # 自适应阈值， 后两个参数 - 卷积核 大小，越大越快； 均匀阀值，不必设置太大，一般10、15左右
        thresh = cv.adaptiveThreshold(warped, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 45, 10)
        cv.imshow("thresh", thresh)

        cv.waitKey(0)
        pass
