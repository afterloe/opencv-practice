#!/usr/bin/python3

import cv2
import imutils

img = cv2.imread("../tmp/3.png", cv2.IMREAD_COLOR)
cv2.imshow("before", img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("gray", gray)
# 骨架化, size 为 结构元素内核大小
skeleton = imutils.skeletonize(gray, size=(3, 3))
cv2.imshow("after", skeleton)

cv2.waitKey(0)
cv2.destroyAllWindows()
