#!/usr/bin/python3

import cv2
import imutils

img = cv2.imread("../tmp/2.jpg", cv2.IMREAD_COLOR)
angleRange = (0, 90, 180, 360)
for angle in angleRange:
    rotated = imutils.rotate(img, angle)
    cv2.imshow("Angle=%d" % (angle), rotated)

cv2.waitKey(0)
cv2.destroyAllWindows()