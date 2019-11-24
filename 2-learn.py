#!/usr/bin/python3

import cv2
import imutils

img = cv2.imread("../tmp/2.jpg", cv2.IMREAD_COLOR)
cv2.imshow("before", img)

# 图像平移
translated = imutils.translate(img, 25, -75)
cv2.imshow("translate", translated)

cv2.waitKey(0)