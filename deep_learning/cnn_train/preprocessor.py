#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from abc import ABC, abstractmethod
from keras.preprocessing.image import img_to_array
import cv2 as cv
import numpy as np
import os
import logging


CONSOLE = logging.getLogger("dev")


class Preprocessor(ABC):

    @abstractmethod
    def pre_process(self, image):
        pass


class ImageToArrayPreprocessor(Preprocessor):

    def __init__(self, dataFormat=None):
        self.__dataFormat = dataFormat

    def pre_process(self, image):
        return img_to_array(image, data_format=self.__dataFormat)


class SimplePreprocessor(Preprocessor):

    def __init__(self, width, height, inter=cv.INTER_AREA):
        self.__width = width
        self.__height = height
        # 插值调整
        self.__inter = inter

    def pre_process(self, image):
        return cv.resize(image, (self.__width, self.__height), interpolation=self.__inter)


class SimpleDatasetLoader(object):

    def __init__(self, preprocessor=None):
        self.__preprocessor = preprocessor
        if None is self.__preprocessor:
            self.__preprocessor = []

    def load(self, image_paths, verbose=-1):
        data = []
        labels = []
        for (i, image_path) in enumerate(image_paths):
            image = cv.imread(image_path)
            label = image_path.split(os.path.sep)[-2]
            if None is not self.__preprocessor:
                for p in self.__preprocessor:
                    image = p.pre_process(image)
            data.append(image)
            labels.append(label)
            if verbose > 0 and i > 0 and 0 == (i + 1) % verbose:
                CONSOLE.info("处理中 ... %d / %d" % (i + 1, len(image_paths)))

        return np.array(data), np.array(labels)
