#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np
import os

WIDTH = 300
HEIGHT = 300


class FaceDetection(object):
    __confidence = 0
    __net, __image = None, None

    def __init__(self, model, prototxt):
        self.__net = cv.dnn.readNetFromCaffe(prototxt, model)

    def setConfidence(self, confidence=0.5):
        self.__confidence = confidence

    def loadImage(self, path_of_image):
        if False is os.path.isfile(path_of_image):
            assert Exception("%s 图像不存在！" % path_of_image)
        image = cv.imread(path_of_image)
        self.__image = cv.resize(image, (WIDTH, HEIGHT))

    def inference(self):
        if None is self.__image:
            assert Exception("执行该函数前请先执行 loadImage(path=str) 进行图像读取")
        h, w = self.__image.shape[: 2]
        blob = cv.dnn.blobFromImage(self.__image, 1.0, (WIDTH, HEIGHT), (104.0, 177.0, 123.0))
        self.__net.setInput(blob)
        detections = self.__net.forwad()
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if self.__confidence < confidence:
                box = detections[0, 0, i, 3: 7] * np.array([w, h, w, h])
                start_x, start_y, end_x, end_y = box.astype("int")
                content = "{:.2f}%".format(confidence * 100)
                y = start_y - 10 if start_y - 10 > 10 else start_y + 10
                cv.rectangle(self.__image, (start_x, start_y), (end_x, end_y), (0, 255, 255), 2)
                cv.putText(self.__image, content, (start_x, y), cv.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0, 0), 2)
        cv.imshow("output", self.__image)
        cv.waitKey(0)
        cv.destroyAllWindows()
