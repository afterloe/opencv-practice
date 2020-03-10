#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
from imutils.video import VideoStream
from imutils.video import FPS
import time


class DebugHelper:

    def __init__(self):
        self._vs = None
        self._fps = None
        self._padding = 300

    def draw_box(self, image):
        if None is image:
            raise Exception("can't draw line in block image!")
        h, w = image.shape[:2]
        x, y, width, height = w // 2 - self._padding // 2, h // 2 - self._padding // 2, self._padding, self._padding
        cv.rectangle(image, (x, y), (x + width, y + height), (0, 0, 255), 2, cv.LINE_AA)
        return image, (x, y, (x + width), (y + height))

    def calibrate_gauge(self):
        self._vs = VideoStream(src=0).start()
        time.sleep(1.0)
        self._fps = FPS().start()
        while True:
            frame = self._vs.read()
            frame_roi, (w, h, width, height) = self.draw_box(frame.copy())
            cv.imshow("user view", frame_roi)
            key = cv.waitKey(10) & 0xff
            if ord("q") == key:
                break
