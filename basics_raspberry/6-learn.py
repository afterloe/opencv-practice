#!/usr/bin/python3

import cv2
import imutils

img = cv2.imread("../tmp/3.png", cv2.IMREAD_COLOR)
cv2.imshow("before", img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edgeMap = imutils.auto_canny(gray)
cv2.imshow("Automatic Edge Map", edgeMap)

cv2.waitKey(0)
cv2.destroyAllWindows()
