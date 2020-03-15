#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import imutils
import os


class ShapeFitting(object):
    def __init__(self, image):
        if False is os.path.isfile(image):
            assert Exception("图像%s不存在" % image)
        self.__image = cv.imread(image)
        self.__color = (240, 0, 159)

    def run(self):
        cv.imshow("input image", self.__image)
        gray = cv.cvtColor(self.__image, cv.COLOR_BGR2GRAY)
        cv.imshow("gray image", gray)
        edged = cv.Canny(gray, 30, 150)
        cv.imshow("edged image", edged)
        # _, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_TRIANGLE)
        thresh = cv.threshold(gray, 225, 255, cv.THRESH_BINARY_INV)[1]
        cv.imshow("thresh", thresh)

        # thresh = cv.erode(thresh, None, iterations=5)
        # thresh = cv.morphologyEx(thresh, cv.MORPH_OPEN, (5, 5))
        cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        for c in cnts:
            cv.drawContours(self.__image, [c], -1, self.__color, 3)
        content = "found %d objects" % len(cnts)
        cv.putText(self.__image, content, (10, 25), cv.FONT_HERSHEY_SIMPLEX, 0.7, self.__color, 2)
        cv.imshow("contours", self.__image)

        output = cv.bitwise_and(self.__image, self.__image, mask=thresh.copy())
        cv.imshow("output", output)

        cv.waitKey(0)
        cv.destroyAllWindows()
