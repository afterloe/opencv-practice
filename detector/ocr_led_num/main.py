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
    edged = cv.Canny(gray, 50, 200, 255)
    cv.imshow("edged", edged)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
