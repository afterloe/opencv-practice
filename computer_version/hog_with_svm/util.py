#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np
from imutils.paths import list_images


class HOGUtil(object):

    def __init__(self):
        pass

    @staticmethod
    def get_descriptor(image):
        hog = cv.HOGDescriptor()
        h, w = image.shape[: 2]
        rate = 64 / w
        image = cv.resize(image, (64, np.int(rate * h)))
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        background = np.zeros((128, 64), dtype=np.uint8)
        background[:, :] = 127
        h, w = gray.shape
        dy = (128 - h) // 2
        background[dy: h + dy, :] = gray
        descriptors = hog.compute(background, winStride=(8, 8), padding=(0, 0))
        return descriptors

    @staticmethod
    def get_data(train_data, labels, path, label_type):
        images_path = list(list_images(path))
        for image_path in images_path:
            image = cv.imread(image_path)
            hog_desc = HOGUtil.get_descriptor(image)
            one_fv = np.zeros([len(hog_desc)], dtype=np.float32)
            for i in range(len(hog_desc)):
                one_fv[i] = hog_desc[i][0]
            train_data.append(one_fv)
            labels.append(label_type)
        return train_data, labels

    @staticmethod
    def get_dataset(pdir, ndir):
        train_data = []
        labels = []
        train_data, labels = HOGUtil.get_data(train_data, labels, pdir, label_type=1)
        train_data, labels = HOGUtil.get_data(train_data, labels, ndir, label_type=-1)
        return np.array(train_data, dtype=np.float32), np.array(labels, dtype=np.int32)
