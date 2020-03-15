#!/usr/bin/env python3
# -*- coding=utf-8 -*-


class FaceDetection(object):
    __confidence = 0
    __model, __protoext = None, None

    def __init__(self, model, prototxt):
        self.__model = model
        self.__protoext = prototxt

    def setConfidence(self, confidence=0.5):
        self.__confidence = confidence
