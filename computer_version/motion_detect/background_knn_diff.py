#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
import cv2 as cv
import imutils
import datetime
from imutils.video import VideoStream, FPS
import logging
import time

__version__ = "1.0.0"

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
CONSOLE = logging.getLogger("dev")
CONSOLE.setLevel(logging.DEBUG)
CONSOLE.info("基础的运动物体检测 %s", __version__)


def run_with_camera(min_area=500):
    bs = cv.createBackgroundSubtractorKNN(detectShadows=True)
    vs = VideoStream(src=0).start()
    time.sleep(2)
    CONSOLE.info("启动视屏监控")
    first_frame = None
    while True:
        frame = vs.read()
        if None is frame:
            CONSOLE.error("can't read any frame from this camera")
            break
        frame = imutils.resize(frame, width=640)
        fg_mask = bs.apply(frame)
        # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # blurred = cv.GaussianBlur(gray, (21, 21), 0)
        # if None is first_frame:
        #     first_frame = blurred
        #     continue
        # frame_delta = cv.absdiff(first_frame, blurred)
        # _, binary = cv.threshold(frame_delta, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
        # _, binary = cv.threshold(fg_mask.copy(), 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
        _, binary = cv.threshold(fg_mask.copy(), 25, 255, cv.THRESH_BINARY)
        # binary = cv.dilate(binary, None, iterations=2)
        binary = cv.erode(binary, None, iterations=2)
        contours = cv.findContours(binary.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        status_text = "None"
        for contour in contours:
            if min_area > cv.contourArea(contour):
                continue
            x, y, w, h = cv.boundingRect(contour)
            cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            status_text = "Occupied"
        cv.putText(frame, "Room Status: %s" % status_text, (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        word = datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p")
        cv.putText(frame, word, (10, frame.shape[0] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        cv.imshow("Security Feed", frame)
        cv.imshow("Thresh", binary)
        # cv.imshow("Frame Delta", frame_delta)
        cv.imshow("fg mask", fg_mask)
        key = cv.waitKey(1) & 0xff
        if ord("q") == key:
            CONSOLE.info("enter q to leave.")
            break
    vs.stop()
    cv.destroyAllWindows()


def run_with_video(video, min_area=500):
    CONSOLE.info("motion video")
    CONSOLE.info(video, min_area)


if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="path of video")
    ap.add_argument("-a", "--min-area", help="minimum area size", type=int, default=500)
    args = vars(ap.parse_args())
    if None is args.get("video", None):
        run_with_camera(min_area=args.get("min_area"))
    else:
        run_with_video(**args)
