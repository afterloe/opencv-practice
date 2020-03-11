#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np
import imutils
from imutils.video import VideoStream

"""

"""

hsv_min, hsv_max = (0, 0, 0), (180, 255, 50)
kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
morphology_param = dict(op=cv.MORPH_OPEN, kernel=kernel)


def process(image):
    hsv = cv.cvtColor(image.copy(), cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, hsv_min, hsv_max)
    blurred = cv.GaussianBlur(mask, (0, 0), 3)
    return blurred
    # cv.imshow("bin", blurred)


def main():
    vs = VideoStream(src=0).start()
    pre_1 = process(vs.read())
    pre_2 = process(vs.read())

    while True:
        frame = vs.read()
        now = process(frame)
        diff_1 = cv.subtract(pre_2, pre_1)
        diff_2 = cv.subtract(now, pre_1)
        diff = cv.bitwise_and(diff_1, diff_2)
        binary = cv.morphologyEx(diff, **morphology_param)
        contours = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        for cnt in contours:
            x, y, w, h = cv.boundingRect(cnt)
            if 100 > h and 100 > w:
                continue
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        pre_1 = np.copy(pre_2)
        pre_2 = np.copy(now)
        cv.imshow("watch dog", frame)
        if None is not diff:
            cv.imshow("dst", diff)
        key = cv.waitKey(100) & 0xff
        if ord("q") == key:
            break
    vs.stop()
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
