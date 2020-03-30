#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import imutils
from imutils.video import VideoStream
import time

"""

"""


def main():
    print("[info] starting video stream ...")
    vs = VideoStream(src=0).start()
    time.sleep(1.0)
    while True:
        frame = vs.read()
        if None is frame:
            break
        cv.imshow("catching....", frame)
        frame = imutils.resize(frame, height=500)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gray = cv.bilateralFilter(gray, 11, 17, 17)
        edged = cv.Canny(gray, 30, 200)
        cv.imshow("edged", edged)
        key = cv.waitKey(1) & 0xff
        if ord("w") == key:
            name = "{}.jpeg".format(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time())))
            path = "pic/{}".format(name)
            cv.imwrite(path, frame, [cv.IMWRITE_JPEG_QUALITY, 100])
            print("[info] image save in {}".format(path))
        if ord("q") == key:
            print("[info] enter q for quit...")
            break
    vs.stop()
    print("[info] wait to leave...")


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
