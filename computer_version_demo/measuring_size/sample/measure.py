#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import imutils
from imutils.contours import sort_contours
import numpy as np
import os


class Measure(object):

    def __init__(self, path_of_image):
        if False is os.path.isfile(path_of_image):
            assert Exception("图像文件不存在")
        self.__image = cv.imread(path_of_image)
        self.__width = 0
        # cv.namedWindow("origin", cv.WINDOW_FREERATIO)

    def set_width(self, width):
        self.__width = width

    def measure_by_object(self):
        gray = cv.cvtColor(self.__image, cv.COLOR_BGR2GRAY)
        blurred = cv.GaussianBlur(gray, (7, 7), 0)
        edged = cv.Canny(blurred, 50, 100)
        edged = cv.dilate(edged, None, iterations=1)
        edged = cv.erode(edged, None, iterations=1)
        contours = cv.findContours(edged, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sort_contours(contours)[0]
        pixls_per_metric = None
        for contour in contours:
            if 100 > cv.contourArea(contour):
                continue
            orig = self.__image.copy()
            box = cv.minAreaRect(contour)
            box = cv.boxPoints(box)
            box = np.array(box, dtype="int")
            cv.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
            for (x, y) in box:
                cv.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)
            cv.imshow("origin", orig)
            cv.waitKey(0)
        pass

    def __del__(self):
        cv.destroyAllWindows()
