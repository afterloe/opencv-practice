#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import imutils

"""

"""

# RESOURCE_PATH = "G:/Project/opencv-ascs-resources/"
RESOURCE_PATH = "/Users/afterloe/Project/opencv-ascs-resources/led-3/"
PADDING = 50


def main():
    image = cv.imread(RESOURCE_PATH + "2020-03-14-18-00.jpeg")
    h, w = image.shape[:2]
    image = image[PADDING: h // 2, :, :]
    cv.imshow("input", image)
    image = imutils.resize(image, height=300)
    blurred = cv.GaussianBlur(image, (9, 9), 0)
    gray = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY)
    edged = cv.Canny(gray, 30, 180)
    cnts = cv.findContours(edged.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    print(len(cnts))
    # for c in cnts:
    #     t = image.copy()
    #     cv.drawContours(t, c, -1, (255, 0, 0), 3)
    #     cv.imshow("t", t)
    #     cv.waitKey(0)
    cv.imshow("image", edged)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
