#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from collections import deque
import cv2 as cv
import imutils
from imutils.video import VideoStream, FPS
import numpy as np
import time


class ObjectTract(object):

    __fps, __loop, __key = None, True, None
    __yellow_lower, __yellow_upper = (26, 43, 46), (34, 255, 255)

    def __init__(self, video, max_buff=64):
        if not video:
            self.__vs = VideoStream(src=0).start()
        else:
            self.__vs = cv.VideoCapture(video)
        self.__video = video
        self.__max_buff = max_buff
        self.__queue = deque(maxlen=max_buff)

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
            # 去除了可能留在面罩上的任何小斑点。 腐蚀2次， 膨胀2次
            mask = cv.erode(mask, None, iterations=2)
            mask = cv.dilate(mask, None, iterations=2)
            contours = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)
            center = None
            if 0 <= len(contours):
                contour = max(contours, key=cv.contourArea)
                (x, y), radius = cv.minEnclosingCircle(contour)
                # 计算轮廓的几何矩
                M = cv.moments(contour)
                # 并根据几何矩获取 轮廓的质心
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                if 10 < radius:
                    cv.circle(frame, (int(x), int(y)), int(radius), (255, 0, 255), 2)
                    cv.circle(frame, center, 5, (0, 0, 255), -1)
            self.__queue.append(center)
            self.draw_track_trajectory(frame)
            cv.imshow("frame", frame)
            cv.imshow("mask", mask)
            self.__key = cv.waitKey(100) & 0xff
            self.process_key()

    def draw_track_trajectory(self, frame):
        for i in range(1, len(self.__queue)):
            if self.__queue[i - 1] is None or self.__queue is None:
                continue
            thickness = int(np.sqrt(self.__max_buff / float(i + 1)) * 2.5)
            cv.line(frame, self.__queue[i - 1], self.__queue[i], (255, 0, 0), thickness)

    def process_key(self):
        if ord("q") == self.__key:
            print("exit to frame")
            self.__loop = False
