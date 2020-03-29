#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import imutils
from imutils import perspective
from unittest import TestCase


class TestDetect(TestCase):

    def setUp(self) -> None:
        orig = cv.imread("../resources/timg_3.jpg")
        image = imutils.resize(orig, width=640)
        self.__image = image
        pass

    def test_plate_detect(self):
        gray = cv.cvtColor(self.__image.copy(), cv.COLOR_BGR2GRAY)
        blurred = cv.GaussianBlur(gray, (7, 7), 0)
        blurred = cv.morphologyEx(blurred, cv.MORPH_OPEN, cv.getStructuringElement(cv.MORPH_RECT, (3, 3)))
        edged = cv.Canny(blurred, 50, 200, 255)
        contours = cv.findContours(edged.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv.contourArea, reverse=True)[: 5]
        display_cnt = None
        for contour in contours:
            peri = cv.arcLength(contour, True)
            approx = cv.approxPolyDP(contour, 0.02 * peri, True)
            if 4 == len(approx):
                display_cnt = approx
                break
        self.detect_character_candidates(display_cnt.reshape(4, 2))
        cv.waitKey(0)

    def detect_character_candidates(self, region):
        plate = perspective.four_point_transform(self.__image, region)
        cv.imshow("perspective transform", imutils.resize(plate, width=400))

    def __del__(self):
        cv.destroyAllWindows()
