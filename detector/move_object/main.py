#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
from imutils.video import VideoStream

"""

"""


def main():
    vs = VideoStream(src=0).start()
    padding, color = 300, (0, 0, 255)
    hsv_min, hsv_max = (0, 0, 0), (180, 255, 50)
    image = vs.read()
    h, w = image.shape[: 2]
    x, y, width, height = w // 2 - padding // 2, h // 2 - padding // 2, padding, padding
    # cv.rectangle(image, (x, y), (x + width, y + height), color, 2, cv.LINE_AA)
    roi = image[y: y + height, x: x + width, :]
    hsv = cv.cvtColor(roi.copy(), cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, hsv_min, hsv_max)
    edged = cv.GaussianBlur(mask, (0, 0), 3)
    hist = cv.calcHist([hsv], [0], edged, [180], [0, 180])
    cv.normalize(hist, hist, 0, 255, cv.NORM_MINMAX)
    while True:
        frame = vs.read()
        roi = frame[y: y + height, x: x + width, :]
        hsv = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
        dst = cv.calcBackProject([hsv], [0], hist, [0, 180], 1)
        track_box = cv.CamShift(dst, (x, y, width, height), (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1))
        print(len(track_box))
        # cv.ellipse(frame, track_box[0], (0, 0, 255), 3, cv.LINE_AA)
        # cv.imshow("watch dog", frame)
        key = cv.waitKey(0) & 0xff
        if ord("q") == key:
            break
    vs.stop()
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
