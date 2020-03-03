#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import imutils
from imutils import contours
from imutils.perspective import four_point_transform
import numpy as np

"""

"""

RESOURCE_PATH = "G:/Project/opencv-ascs-resources/"


def main():
    image = cv.imread(RESOURCE_PATH + "led-2/2020-03-03_21-04-17.jpeg")
    cv.imshow("input", image)
    # ratio = image.shape[0] / 500.0
    image = imutils.resize(image, width=1000)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (9, 9), 0)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    gray = cv.morphologyEx(gray, cv.MORPH_OPEN, kernel)
    edged = cv.Canny(blurred, 20, 120)
    cnts = cv.findContours(edged.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    print(len(cnts))
    cnts = sorted(cnts, key=cv.contourArea, reverse=True)[:10]
    # screen_cnt = None
    # for c in cnts:
    #     peri = cv.arcLength(c, True)
    #     print(peri)
    #     approx = cv.approxPolyDP(c, peri * 0.12, True)
    #     if len(approx) == 4:
    #         screen_cnt = approx
    #         # break

    cv.drawContours(image, cnts, -1, (0, 255, 0), 3)
    cv.imshow("led", image)
    cv.imshow("edged", edged)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
