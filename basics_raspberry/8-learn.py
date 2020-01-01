#!/usr/bin/env python
# coding=utf-8
# python3 默认utf-8编码， python2.x需要指定编码

from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2

"""
参数解释器 初始化
"""
ap = argparse.ArgumentParser()
ap.add_argument("-v", "-video", help="path to the video file")
ap.add_argument("-a", "-min_area", type=int, default=50, help="minimum area size")
args = vars(ap.parse_args())

"""
{v: None, a: 50}
"""
# print(args)

if None is args.get("v"):
    # 使用imutils 的视频播放方法， 非opencv
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
else:
    vs = cv2.VideoCapture(args["v"])

# 初始化
firstFrame = None

while True:
    frame = vs.read()
    frame = frame if args.get("v", None) is None else frame[1]
    text = "Unoccupied"
    if None is frame:
        break

    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Ksize(width, height) 必须为大于零的 奇数， width 与 height可以不同
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    if None is firstFrame:
        firstFrame = gray
        continue
    # 当前帧 与前一帧进行对比
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    # 对图像进行 膨胀处理， 确定差值所在位置
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    for c in cnts:
        # 对内容进行过滤， 当差值面积小于 设定阈值时 过滤
        if cv2.contourArea(c) < args["a"]:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + w), (0, 255, 0), 2)
        text = "Occupied"

    # 对画面打上 时间戳
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    """
        Y - （1xxx）年 |  m - （12）月 | d - (30) 日 | H - （24）小时 | M - （60）分钟 | S - （60）秒
    """
    cv2.putText(frame, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF
    if ord("q") == key:
        break

vs.stop() if None is args.get("v", None) else vs.release()
cv2.destroyAllWindows()