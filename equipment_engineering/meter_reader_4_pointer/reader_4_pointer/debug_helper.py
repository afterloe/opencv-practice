#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
from .current_util import avg_circles
from imutils.video import VideoStream
from imutils.video import FPS
from .logger import log, LOG_SAVE_PATH, get_time_str
from .process_util import draw_box, draw_gauge, meter_detection, pointer_detection, infer
import time


class DebugHelper:

    _vs, _roi, _fps, _key, _save_image_with_box, _save_image_with_gauge = None, None, None, None, None, None
    _content = "wait to read ... ..."

    def __init__(self, argument):
        self._min_angle, self._max_angle, self._min_value, self._max_value, self._util = argument

    def process_with_key(self) -> None:
        if ord("q") == self._key:
            log("准备退出程序")
            self._vs.stop()
            cv.destroyAllWindows()
        if ord("w") == self._key:
            log("调试图像保存在 %s" % LOG_SAVE_PATH)
            cv.imwrite("%s_%s_%s" % (LOG_SAVE_PATH, "image_with_box", get_time_str()), self._save_image_with_box,
                       [cv.IMWRITE_JPEG_QUALITY, 100])
            cv.imwrite("%s_%s_%s" % (LOG_SAVE_PATH, "image_with_gauge", get_time_str()), self._save_image_with_gauge,
                       [cv.IMWRITE_JPEG_QUALITY, 100])
            cv.imwrite("%s_%s_%s" % (LOG_SAVE_PATH, "image_with_roi", get_time_str()), self._roi,
                       [cv.IMWRITE_JPEG_QUALITY, 100])

    def run(self, device):
        self._vs = VideoStream(src=device, usePiCamera=True).start()
        time.sleep(1.0)
        self._fps = FPS().start()
        while True:
            frame = self._vs.read()
            frame_with_box, (x, y, w, h) = draw_box(frame)
            self._roi = frame[y: h, x: w, :]
            cv.putText(frame_with_box, self._content, (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                       (0, 255, 255), 2, cv.LINE_AA)
            cv.imshow("debug view", frame_with_box)
            self._key = cv.waitKey(100) & 0xff
            self.process_with_key()
            flag, meter = meter_detection(self._roi)
            if False is flag:
                self._content = "meter lose ... ..."
                continue
            flag, roi_with_gauge = draw_gauge(meter, self._roi)
            if False is flag:
                continue
            cv.imshow("gauge", roi_with_gauge)
            a, b, c = meter.shape
            meter_x, meter_y, meter_r = avg_circles(meter, b)
            flag, pointer = pointer_detection(self._roi, (meter_x, meter_y, meter_r))
            if False is flag:
                self._content = "pointer loser ... ..."
                continue
            a1, b1, c1, d1 = pointer
            cv.putText(frame_with_box,  "start", (a1 + x, b1 + y),
                       cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2, cv.LINE_AA)
            cv.putText(frame_with_box, "end", (c1 + x, d1 + y),
                       cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2, cv.LINE_AA)
            cv.line(frame_with_box, (pointer[0] + x, pointer[1] + y), (pointer[2] + x, pointer[3] + y), (0, 0, 255),
                    5, cv.LINE_AA)
            value = infer(meter_x, meter_y, pointer, self._min_angle, self._max_angle, self._min_value, self._max_value)
            if value < self._min_value or value > self._max_value:
                self._content = "out of rang!"
                continue
            self._content = "{:.3f} {}".format(value, self._util)
            self._save_image_with_box = frame_with_box
            self._save_image_with_gauge = roi_with_gauge
            log(self._content)
