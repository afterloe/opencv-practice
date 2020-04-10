#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
import imutils
import datetime
from imutils.video import VideoStream, FPS
import sys
import time
import cv2 as cv


def application(video, min_area=500):
    if None is not video:
        print("加载本地视频")
        sys.exit(1)
    avg = None
    vs = VideoStream(src=0).start()
    time.sleep(2)
    while True:
        timestamp = datetime.datetime.now()
        frame = vs.read()
        if None is frame:
            print("can't read any video from src=0")
            break
        frame = imutils.resize(frame, width=640)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        blurred = cv.GaussianBlur(gray, (21, 21), 0)
        if None is avg:
            print("Starting background model")
            avg = gray.copy().astype("float")
            continue
        cv.accumulateWeighted(blurred, avg, 0.5)
        frame_delta = cv.absdiff(blurred, cv.convertScaleAbs(avg))
        _, binary = cv.threshold(frame_delta, 25, 255, cv.THRESH_BINARY)
        binary = cv.dilate(binary, None, iterations=2)
        contours = cv.findContours(binary.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        for contour in contours:
            if min_area > cv.contourArea(contour):
                continue
            time_text = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
            print("%s Occupied" % time_text)
            x, y, w, h = cv.boundingRect(contour)
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            cv.putText(frame, time_text, (10, frame.shape[0] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.35, (255, 0, 0), 1)
        cv.imshow("frame_delta", frame_delta)
        cv.imshow("monitor", frame)
        key = cv.waitKey(1) & 0xff
        if ord("q") == key:
            print("enter q to leave")
            break
    cv.destroyAllWindows()
    vs.stop()


if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="load local video")
    ap.add_argument("-m", "--min-area", type=int, help="minimum area size", default=500)
    args = vars(ap.parse_args())
    application(**args)
