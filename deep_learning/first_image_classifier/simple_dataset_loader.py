#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import numpy as np
import cv2 as cv
import os
import logging

CONSOLE = logging.getLogger("dev")


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
