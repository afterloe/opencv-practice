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


class TrainLeNet(object):

    def __init__(self):
        pass

    def __del__(self):
        pass

    def run(self):
        pass
