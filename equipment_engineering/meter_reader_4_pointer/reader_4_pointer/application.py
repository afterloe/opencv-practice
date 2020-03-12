#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from .current_util import mean_shift_filtering
import cv2 as cv
from imutils.video import FPS
from imutils.video import VideoStream
from .logger import log, ERROR
import numpy as np
from .process_util import draw_box, infer_diff, meter_detection, pointer_detection, avg_circles, infer
import time


class Application:

    def __init__(self, argument):
        self._vs, self._fps, self._flag, self._roi_previous, self._roi = None, None, True, None, None
        self._min_angle, self._max_angle, self._min_value, self._max_value, self._util = argument
        self._value, self._flag_infer_diff = 0.0, False

    def argument_process(self):
        self._min_angle = float(self._min_angle)
        self._max_angle = float(self._max_angle)
        self._min_value = float(self._min_value)
        self._max_value = float(self._max_value)

    def run(self, device=0, vision=True) -> None:
        self._vs = VideoStream(src=device).start()
        time.sleep(1.0)
        self.argument_process()
        self._fps = FPS().start()
        while self._flag:
            frame = self._vs.read()
            frame_with_box, (x, y, w, h) = draw_box(frame)
            self._roi = frame[y: h, x: w, :]
            # flag, binary_now = infer_diff(self._roi_previous, self._roi)
            # if False is flag or True is self._flag_infer_diff:
            #     self._flag_infer_diff = False
            #     continue
            # self._roi_previous = binary_now
            flag, meter = meter_detection(self._roi)
            if False is flag:
                continue
            a, b, c = meter.shape
            meter_x, meter_y, meter_r = avg_circles(meter, b)
            flag, pointer = pointer_detection(self._roi, (meter_x, meter_y, meter_r))
            if False is flag:
                continue
            value = infer(meter_x, meter_y, pointer, self._min_angle, self._max_angle, self._min_value, self._max_value)
            if value < self._min_value or value > self._max_value:
                self._flag_infer_diff = True
                continue
            # flag = mean_shift_filtering(value)
            # if True is flag:
            #     self._flag_infer_diff = True
            #     continue
            log("value is {:.3f} {}".format(value, self._util))
            if vision:
                a1, b1, c1, d1 = pointer
                cv.putText(self._roi, "start", (a1, b1),
                           cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2, cv.LINE_AA)
                cv.putText(self._roi, "end", (c1, d1),
                           cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2, cv.LINE_AA)
                cv.line(self._roi, (pointer[0], pointer[1]), (pointer[2], pointer[3]), (0, 0, 255), 5, cv.LINE_AA)
                cv.putText(frame_with_box, "{:.3f} {}".format(value, self._util), (x, y),
                           cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2, cv.LINE_AA)
                cv.imshow("watch dog", frame_with_box)
            key = cv.waitKey(100) & 0xff
            self.process_with_key(key, vision)

    def process_with_key(self, key, vision) -> None:
        if ord("q") == key:
            log("准备退出程序")
            self._flag = False
            self._vs.stop()
            if vision:
                cv.destroyAllWindows()
