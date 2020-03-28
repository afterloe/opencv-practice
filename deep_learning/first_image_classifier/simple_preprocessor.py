#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv


class SimplePreprocessor(object):

    def __init__(self, width, height, inter=cv.INTER_AREA):
        self.__width = width
        self.__height = height
        # 插值调整
        self.__inter = inter

    def pre_process(self, image):
        return cv.resize(image, (self.__width, self.__height), interpolation=self.__inter)
