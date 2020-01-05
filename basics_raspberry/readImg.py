#!/usr/bin/python3

import cv2

WINDOW_NAME = "picImage"

img = cv2.imread("G:/learn-project/tmp/1.jpg", cv2.IMREAD_COLOR)
cv2.imshow("picImage", img)
cv2.waitKey(0)

print("image is closed!")
