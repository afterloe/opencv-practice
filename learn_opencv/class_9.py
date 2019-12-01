#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

gray = cv.imread("G:/pic/gray.png", cv.IMREAD_GRAYSCALE)
cv.imshow("gray", gray)

min_v, max_v, min_loc, max_loc = cv.minMaxLoc(gray)
print("min: %.3f, max: %.3f" % (min_v, max_v))
print("min loc: ", min_loc)
print("max loc: ", max_loc)

means, stddev = cv.meanStdDev(gray)
print("mean: %.3f, stddev: %.3f" % (means, stddev))

gray[np.where(gray < means)] = 0
gray[np.where(gray > means)] = 255

cv.imshow("binary", gray)

print("------------------------------->>> 3 channel pic")

src = cv.imread("G:/pic/rmb/100.png")
cv.imshow("input", src)

#min_v, max_v, min_loc, max_loc = cv.minMaxLoc(src)
print("min: %.3f, max: %.3f" % (min_v, max_v))
print("min loc: ", min_loc)
print("max loc: ", max_loc)

#means, stddev = cv.meanStdDev(src)
#print("blue channel ->> mean: %.3f, stddev: %.3f" % (means[0], stddev[0]))
#print("green channel ->> mean: %.3f, stddev: %.3f" % (means[1], stddev[1]))
#print("red channel ->> mean: %.3f, stddev: %.3f" % (means[2], stddev[2]))


cv.waitKey(0)
cv.destroyAllWindows()
