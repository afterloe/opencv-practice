#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import logging
import matplotlib

matplotlib.use("Agg")

from keras.preprocessing.image import ImageDataGenerator, img_to_array
from keras.optimizers import Adam
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from imutils import paths
from .lenet import LeNet
import matplotlib.pyplot as plt
import numpy as np
import random
import cv2 as cv
import os

CONSOLE = logging.getLogger("dev")

EPOCHS = 25
INIT_LR = 1e-3
BS = 32


class TrainLeNet(object):

    def __init__(self, path_of_images):
        self.__data = []
        self.__labels = []
        self.__path_of_images = sorted(list(paths.list_images(path_of_images)))
        random.seed(42)
        random.shuffle(path_of_images)
        pass

    def __del__(self):
        pass

    def run(self):
        for image_path in self.__path_of_images:
            image = cv.imread(image_path)
            image = cv.resize(image, (28, 28))
            image = img_to_array(image)
            self.__data.append(image)
            label = image_path.split(os.path.sep)[-2]
            label = 1 if label == "nazha" else 0
            self.__labels.append(label)
        pass
