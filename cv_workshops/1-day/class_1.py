#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv

src = cv.imread("G:/pic/5yuan.jpg")
cv.namedWindow("input", cv.WINDOW_AUTOSIZE)
cv.imshow("input", src)
cv.waitKey(0)
cv.destroyAllWindows()