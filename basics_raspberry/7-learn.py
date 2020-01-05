#!/usr/bin/python

from imutils import perspective
import numpy as np
import cv2

img = cv2.imread("../tmp/2.jpg", cv2.IMREAD_COLOR)
img_clone = img.copy()

cv2.imshow("before", img_clone)
pts = np.array([(73, 239), (356, 117), (475, 265), (187, 443)])

for (x, y) in pts:
    cv2.circle(img_clone, (x, y), 5, (0, 255, 0), -1)

warped = perspective.four_point_transform(img, pts)

cv2.imshow("after", warped)
cv2.waitKey(0)
cv2.destroyAllWindows()