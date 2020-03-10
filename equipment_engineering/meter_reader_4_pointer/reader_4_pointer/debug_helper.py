#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import time


class DebugHelper:

    def __init__(self):
        self._vs = None
        self._fps = None
        self._padding = 300
        self._separation = 10

    def draw_box(self, image):
        if None is image:
            raise Exception("can't draw line in block image!")
        h, w = image.shape[:2]
        x, y, width, height = w // 2 - self._padding // 2, h // 2 - self._padding // 2, self._padding, self._padding
        cv.rectangle(image, (x, y), (x + width, y + height), (0, 0, 255), 2, cv.LINE_AA)
        return image, (x, y, (x + width), (y + height))

    def avg_circles(self, circles, b):
        avg_x, avg_y, avg_r = 0, 0, 0
        for i in range(b):
            avg_x = avg_x + circles[0][i][0]
            avg_y = avg_y + circles[0][i][1]
            avg_r = avg_r + circles[0][i][2]
        return int(avg_x / b), int(avg_y / b), int(avg_r / b)

    def draw_gauge(self, image):
        height, width = image.shape[: 2]
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 20, np.array([]), 100, 50,
                                  int(height * 0.35), int(height * 0.48))
        if 3 != len(circles.shape):
            return image
        a, b, c = circles.shape
        x, y, r = self.avg_circles(circles, b)
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
        text_offset_x = 10
        text_offset_y = 5
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
        return image

    def calibrate_gauge(self):
        self._vs = VideoStream(src=0).start()
        time.sleep(1.0)
        self._fps = FPS().start()
        while True:
            frame = self._vs.read()
            frame_with_roi, (w, h, width, height) = self.draw_box(frame.copy())
            gauge_roi = self.draw_gauge(frame[h: height, w: width, :].copy())
            cv.imshow("computer vision", gauge_roi)
            
            # frame_with_roi[h: height, w: width, :] = gauge_roi
            cv.imshow("user view", frame_with_roi)
            key = cv.waitKey(10) & 0xff
            if ord("q") == key:
                break
