#!/usr/bin/python3

import cv2
import imutils

img = cv2.imread("../tmp/2.jpg", cv2.IMREAD_COLOR)
for width in (400, 300, 200, 100):
    resized = imutils.resize(img, width = width)
    cv2.imshow("Width = %d" % (width), resized)

cv2.waitKey(0)
cv2.destroyAllWindows()