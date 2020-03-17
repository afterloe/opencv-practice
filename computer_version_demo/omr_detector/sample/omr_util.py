#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import imutils
from imutils.perspective import four_point_transform
import os


class OMRUtil(object):
    __step = 300

    def __init__(self, path_of_image="resources/demo.png"):
        if not os.path.isfile(path_of_image):
            print("can't find any image")
            exit(0)
        self.__image = cv.imread(path_of_image)

    def run(self):
        h, w = self.__image.shape[: 2]
        ratio = h / float(self.__step)
        image = imutils.resize(self.__image, height=self.__step)
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        blurred = cv.bilateralFilter(gray, 5, 17, 17)
        edged = cv.Canny(blurred, 75, 200)
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
        warped = four_point_transform(self.__image, screen_cnt.reshape(4, 2) * ratio)
        cv.imshow("output", warped)
        cv.waitKey(0)

    def detector(self):
        h, w = self.__image.shape[: 2]
        ratio = h / float(self.__step)
        image = imutils.resize(self.__image, height=self.__step)
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        blurred = cv.bilateralFilter(gray, 5, 20, 20)
        edged = cv.Canny(blurred, 70, 200)
        contours = cv.findContours(edged, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv.contourArea, reverse=True)[: 3]
        paper_contour = None
        for contour in contours:
            peri = cv.arcLength(contour, True)
            approx = cv.approxPolyDP(contour, 0.05 * peri, True)
            if 4 == len(approx):
                paper_contour = contour
                break
        if None is paper_contour:
            print("can't find paper!")
            return
        warped = four_point_transform(self.__image, paper_contour.reshape(4, 2) * ratio)
        cv.imshow("output", warped)
        cv.waitKey(0)
        pass

    def infer(self):
        pass

    def __del__(self):
        cv.destroyAllWindows()
