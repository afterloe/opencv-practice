#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
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
