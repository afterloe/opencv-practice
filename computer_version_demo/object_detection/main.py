#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
from imutils.video import VideoStream, FPS
import imutils
import numpy as np
import time
import cv2 as cv
import logging

__version__ = "1.0.0"

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
CONSOLE = logging.getLogger("dev")
CONSOLE.setLevel(logging.DEBUG)
CONSOLE.info("实时对象检测 %s", __version__)

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--prototxt", required=True, help="Caffe 模型部署描述文件")
    ap.add_argument("-m", "--model", required=True, help="Caffe 模型")
    ap.add_argument("-c", "--confidence", type=float, default=0.5, help="阈值")
    args = vars(ap.parse_args())

    CONSOLE.info("加载模型")
    net_model = cv.dnn.readNetFromCaffe(args["prototxt"], args["model"])
    CONSOLE.info("加载视频")
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    fps = FPS().start()
    while True:
        frame = vs.read()
        if None is frame:
            CONSOLE.error("无法读取视频流")
            break
        frame = imutils.resize(frame, width=400)
        h, w = frame[: 2]
        blob_data = cv.dnn.blobFromImage(cv.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        net_model.setInput(blob_data)
        detections = net_model.forward()
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if args["confidence"] < confidence:
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3: 7] * np.array([w, h, w, h])
                start_x, start_y, end_x, end_y = box.astype("int")
                content = "%s: %.2f%%" % (CLASSES[idx], confidence * 100)
                cv.rectangle(frame, (start_x, start_y), (end_x, end_y), COLORS[idx], 2)
                y = start_y - 15 if 15 < start_y - 15 else start_y + 15
                cv.putText(frame, content, (start_x, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
        cv.imshow("frame", frame)
        key = cv.waitKey(1) & 0xff
        if ord("q") == key:
            CONSOLE.info("退出监控")
            break
        fps.update()
    fps.stop()
    CONSOLE.info("视频播放时间: %.2f" % fps.elapsed())
    CONSOLE.info("平均FPS: %.2f" % fps.fps())
    cv.destroyAllWindows()
    vs.stop()
