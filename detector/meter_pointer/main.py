#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import imutils
from imutils.object_detection import non_max_suppression
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import time

"""

"""

PATH_OF_NET_BIN = "../../../raspberry-auto/models/yolo/yolov3-tiny.weights"
PATH_OF_NET_CONFIG = "../../../raspberry-auto/models/yolo/yolov3-tiny.cfg"


def log(message, log_type="INFO"):
    content = "[{}][{}]: {}".format(log_type, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), message)
    print(content)
    return content


def detector_meter(image, net, out_names=None):
    image = imutils.resize(image, width=416)
    h, w = image.shape[:2]
    data = cv.dnn.blobFromImage(image, 1.0 / 255.0, (416, 416), None, False, False)
    net.setInput(data)
    outs = net.forward(out_names)
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            if class_id != 74:
                continue
            confidence = scores[class_id]
            if 0.5 < confidence:
                center_x = int(detection[0] * w)
                center_y = int(detection[1] * h)
                width = int(detection[2] * w)
                height = int(detection[3] * h)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                confidences.append(float(confidence))
                boxes.append((left, top, width, height))
    targets = non_max_suppression(np.array(boxes), probs=confidences)
    for left, top, width, height in targets:
        cv.rectangle(image, (left, top), (left + width, top + height), (0, 0, 255), 2, cv.LINE_AA)
        cv.putText(image, "target", (left, top), cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 2)
    cv.imshow("target", image)


def main():
    vs = None
    # try:
    log("load net from disk in {}".format(PATH_OF_NET_BIN))
    dnn = cv.dnn.readNetFromDarknet(PATH_OF_NET_CONFIG, PATH_OF_NET_BIN)
    layout_name = dnn.getUnconnectedOutLayersNames()
    log("starting video steam ... ...")
    vs = VideoStream(src=0).start()
    time.sleep(1.0)
    fps = FPS().start()
    while True:
        frame = vs.read()
        if None is frame:
            log("can't read any video frame from device-0", "ERROR")
            raise Exception()
        detector_meter(frame, dnn, layout_name)
        key = cv.waitKey(50) & 0xff
        if ord("q") == key:
            log("enter q to quit ...")
            break
        fps.stop()
        log("elapsed time: {:.2f}".format(fps.elapsed()))
        log("approx. FPS: {:.2f}".format(fps.fps()))
    # except Exception as e:
    #     print(e)
    # finally:
    log("stop qt for python ... ...")
    cv.destroyAllWindows()
    if None is not vs:
        log("stop video steam ... ...")
        vs.stop()


if "__main__" == __name__:
    main()
