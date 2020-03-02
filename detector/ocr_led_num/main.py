#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import imutils
from imutils import contours
from imutils.perspective import four_point_transform
import numpy as np

"""

"""


def main():
    image = cv.imread("G:/Project/opencv-ascs-resources/led/2020-03-02_21-36-07.jpeg")
    cv.imshow("input", image)
    image = imutils.resize(image, width=500)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (3, 3), 0)
    t = 20
    edged = cv.Canny(blurred, t, t * 2)
    # edged = cv.adaptiveThreshold(ed, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 10)
    cnts = cv.findContours(edged.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # 轮廓排序
    cnts = sorted(cnts, key=cv.contourArea, reverse=False)
    for c in cnts:
        t = image.copy()
        cv.drawContours(t, c, 0, (0, 255, 0))
        cv.imshow("dist", t)
        cv.waitKey(0)

    cv.imshow("edged", edged)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
