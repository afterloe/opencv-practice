#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
from imutils.video import FPS
from imutils.video import VideoStream
from .logger import log, ERROR
from .process_util import draw_box, infer_diff, meter_detection, avg_circles, infer
import time


class Application:

    def __init__(self, argument):
        self._vs = None
        self._fps = None
        self._flag = True
        self._roi_previous = None
        self._min_angle, self._max_angle, self._min_value, self._max_value, self._util = argument

    def run(self, device=0, vision=True) -> None:
        self._vs = VideoStream(src=device).start()
        time.sleep(1.0)
        self._fps = FPS().start()
        while self._flag:
            frame = self._vs.read()
            frame_with_box, (x, y, w, h) = draw_box(frame)
            roi_next = frame[y: h, x: w, :]
            flag, previous = infer_diff(self._roi_previous, roi_next)
            if vision:
                cv.imshow("watch dog", frame_with_box)
            if False is flag:
                continue
            self._roi_previous = previous
            flag, meter = meter_detection(roi_next)
            if False is flag:
                continue
            flag, pointer = pointer_detection(roi_next)
            if False is flag:
                continue
            a, b, c = meter.shape
            x, y, _ = avg_circles(meter, b)
            value = infer(x, y, pointer, self._min_angle, self._max_angle, self._min_value, self._max_value)
            log("value is {:.3f} {}".format(value, self._util))
            if vision:
                cv.putText(frame_with_roi, "{:.3f} {}".format(value, self._util), (w, h),
                           cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2, cv.LINE_AA)
            key = cv.waitKey(100) & 0xff
            self.process_with_key(key, vision)

    def process_with_key(self, key, vision) -> None:
        if ord("q") == key:
            log("准备退出程序")
            self._flag = False
            self._vs.stop()
            if vision:
                cv.destroyAllWindows()
