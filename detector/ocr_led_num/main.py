#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import imutils
from imutils.video import VideoStream
from imutils import contours
from imutils.perspective import four_point_transform
import numpy as np
import time

"""

"""

PADDING = 200


def log(message, log_type="INFO"):
    content = "[{}][{}]: {}".format(log_type, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), message)
    print(content)
    return content


def draw_line(image):
    if None is image:
        raise Exception("can't draw line in block image!")
    h, w = image.shape[:2]
    x, y, width, height = w // 2 - PADDING // 2, h // 2 - PADDING // 2, PADDING, PADDING
    cv.rectangle(image, (x, y), (x + width, y + height), (0, 0, 255), 2, cv.LINE_AA)
    return image, (x, y, (x + width), (y + height))


def produce_roi(roi, width, height):
    image = imutils.resize(roi, width=500)
    ratio = image.shape[1] / 300.0
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.bilateralFilter(gray, 11, 17, 17)
    blurred = cv.GaussianBlur(gray, (11, 11), 0)
    threshed = cv.threshold(blurred.copy(), 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 13))
    threshed = cv.morphologyEx(threshed, cv.MORPH_CLOSE, kernel)
    cnts = cv.findContours(threshed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # cnts = sorted(cnts, key=cv.contourArea, reverse=True)
    digit_cnts = []
    for cnt in cnts:
        x, y, w, h = cv.boundingRect(cnt)
        if w >= 3 and (60 <= h <= 200):
            digit_cnts.append(cnt)
        #     cv.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv.imshow("threshed", threshed)
    cv.imshow("roi", image)
    if 0 == len(digit_cnts):
        return
    digit_cnts = contours.sort_contours(digit_cnts, method="left-to-right")[0]
    for cnt in digit_cnts:
        x, y, w, h = cv.boundingRect(cnt)
        name = "{}.jpeg".format(int(time.time()))
        path = "../collect/pic/{}".format(name)
        cv.imwrite(path, threshed[y: y + h, x: x + w], [cv.IMWRITE_JPEG_QUALITY, 100])
        print("[info] image save in {}".format(path))


def main():
    log("starting video stream ...")
    vs = VideoStream(src=0).start()
    time.sleep(1.0)
    try:
        while True:
            frame = vs.read()
            frame, (w, h, width, height) = draw_line(frame)
            produce_roi(frame[h: height, w: width, :], width, height)
            # cv.imshow("number detector", frame)
            key = cv.waitKey(10) & 0xff
            if ord("q") == key:
                log("wait to quit ...")
                break
    except Exception as e:
        # print(e)
        log(e, "ERROR")
    finally:
        vs.stop()
        cv.destroyAllWindows()


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
