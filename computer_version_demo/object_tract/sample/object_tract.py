#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import imutils
from imutils.video import VideoStream, FPS
import time


class ObjectTract(object):

    __fps, __loop, __key = None, True, None
    __yellow_lower, __yellow_upper = (26, 43, 46), (34, 255, 255)

    def __init__(self, video, max_buff=64):
        self.__max_buf = max_buff
        if not video:
            self.__vs = VideoStream(src=0).start()
        else:
            self.__vs = cv.VideoCapture(video)
        self.__video = video

    def __del__(self):
        cv.destroyAllWindows()
        if not self.__video:
            self.__vs.stop()
        else:
            self.__vs.release()

    def start_track(self):
        print("begin to track")
        time.sleep(1.0)
        while self.__loop:
            frame = self.__vs.read()
            frame = frame[1] if self.__video else frame
            if None is frame:
                print("video can't read")
                break
            frame = imutils.resize(frame, width=600)
            blurred = cv.GaussianBlur(frame, (11, 11), 0)
            hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)
            mask = cv.inRange(hsv, self.__yellow_lower, self.__yellow_upper)
            mask = cv.erode(mask, None, iterations=2)
            mask = cv.dilate(mask, None, iterations=2)
            cv.imshow("frame", frame)
            cv.imshow("mask", mask)
            self.__key = cv.waitKey(100) & 0xff
            self.process_key()

    def process_key(self):
        if ord("q") == self.__key:
            print("exit to frame")
            self.__loop = False
