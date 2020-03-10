#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
from .current_util import avg_circles, calculate_distance
from imutils.video import VideoStream
from imutils.video import FPS
from .logger import log
import numpy as np
import time


class DebugHelper:

    def __init__(self, argument):
        self._vs = None
        self._fps = None
        self._padding = 300
        self._separation = 10
        self._x, self._y = 0, 0
        self._min_angle, self._max_angle, self._min_value, self._max_value = argument

    def draw_box(self, image):
        if None is image:
            raise Exception("can't draw line in block image!")
        h, w = image.shape[:2]
        x, y, width, height = w // 2 - self._padding // 2, h // 2 - self._padding // 2, self._padding, self._padding
        cv.rectangle(image, (x, y), (x + width, y + height), (0, 0, 255), 2, cv.LINE_AA)
        return image, (x, y, (x + width), (y + height))

    def draw_gauge(self, image):
        height, width = image.shape[: 2]
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 20, np.array([]), 100, 50,
                                  int(height * 0.35), int(height * 0.48))
        if 3 != len(circles.shape):
            return image, False
        a, b, c = circles.shape
        x, y, r = avg_circles(circles, b)
        self._x, self._y = x, y
        cv.circle(image, (x, y), r, (0, 0, 255), 3, cv.LINE_AA)
        cv.circle(image, (x, y), 2, (0, 255, 255), 3, cv.LINE_AA)
        interval = int(360 / self._separation)
        p1, p2, p_text = np.zeros((interval, 2)), np.zeros((interval, 2)), np.zeros((interval, 2))
        for i in range(0, interval):
            for j in range(0, 2):
                if 0 == j % 2:
                    p1[i][j] = x + 0.9 * r * np.cos(self._separation * i * np.pi / 180)
                else:
                    p1[i][j] = y + 0.9 * r * np.sin(self._separation * i * np.pi / 180)
        text_offset_x, text_offset_y = 10, 5
        for i in range(0, interval):
            for j in range(0, 2):
                if 0 == j % 2:
                    p2[i][j] = x + r * np.cos(self._separation * i * np.pi / 180)
                    p_text[i][j] = x - text_offset_x + 1.2 * r * np.cos(self._separation * (i + 9) * np.pi / 180)
                else:
                    p2[i][j] = y + r * np.sin(self._separation * i * np.pi / 180)
                    p_text[i][j] = y + text_offset_y + 1.2 * r * np.sin(self._separation * (i + 9) * np.pi / 180)
        for i in range(0, interval):
            cv.line(image, (int(p1[i][0]), int(p1[i][1])), (int(p2[i][0]), int(p2[i][1])), (0, 255, 0), 2)
            cv.putText(image, "%s" % (int(i * self._separation)), (int(p_text[i][0]), int(p_text[i][1])),
                       cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv.LINE_AA)
        return image, True

    def infer_value(self, roi):
        hsv = cv.cvtColor(roi.copy(), cv.COLOR_BGR2HSV)
        hsv_min = (0, 0, 0)
        hsv_max = (180, 255, 50)
        mask = cv.inRange(hsv, hsv_min, hsv_max)
        lines = cv.HoughLinesP(mask, 1, np.pi / 180, 100, None, 30, 10)
        if None is lines:
            log("未检测到指针")
            return 0, roi
        x1, y1, x2, y2 = lines[0][0]
        cv.line(roi, (x1, y1), (x2, y2), (0, 0, 255), 5, cv.LINE_AA)
        dist_pt_0 = calculate_distance(self._x, self._y, x1, y1)
        dist_pt_1 = calculate_distance(self._x, self._y, x2, y2)
        if dist_pt_0 > dist_pt_1:
            x_angle, y_angle = x1 - self._x,  self._y - y1
        else:
            x_angle, y_angle = x2 - self._x, self._y - y2
        res = np.arctan(np.divide(float(y_angle), float(x_angle)))
        res = np.rad2deg(res)
        final_angle = 0
        if x_angle > 0 and y_angle > 0:  # in quadrant I
            final_angle = 270 - res
        if x_angle < 0 and y_angle > 0:  # in quadrant II
            final_angle = 90 - res
        if x_angle < 0 and y_angle < 0:  # in quadrant III
            final_angle = 90 - res
        if x_angle > 0 and y_angle < 0:  # in quadrant IV
            final_angle = 270 - res
        old_min, old_max = float(self._min_angle), float(self._max_angle)
        new_min, new_max = float(self._min_value), float(self._max_value)
        old_value = final_angle
        old_range = old_max - old_min
        new_range = new_max - new_min
        new_value = (((old_value - old_min) * new_range) / old_range) + new_min
        return new_value, roi

    def calibrate_gauge(self):
        self._vs = VideoStream(src=0).start()
        time.sleep(1.0)
        self._fps = FPS().start()
        while True:
            frame = self._vs.read()
            frame_with_roi, (w, h, width, height) = self.draw_box(frame.copy())
            gauge_roi, flag = self.draw_gauge(frame[h: height, w: width, :].copy())
            cv.imshow("computer vision for gauge", gauge_roi)
            if flag:
                value, gauge_roi = self.infer_value(frame[h: height, w: width, :].copy())
                cv.imshow("computer vision for pointer", gauge_roi)
                print(value)
            cv.imshow("user view", frame_with_roi)
            key = cv.waitKey(10) & 0xff
            if ord("q") == key:
                break
