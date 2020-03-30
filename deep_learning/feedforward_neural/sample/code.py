#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
from .funs import image_to_feature_vector
from imutils import paths
from keras.utils import np_utils
from keras.models import Sequential
from keras.optimizers import SGD
from keras.layers import Dense, Activation
import logging
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

CONSOLE = logging.getLogger("dev")


class Code(object):

    def __init__(self, image_path):
        if False is os.path.isdir(image_path):
            assert Exception("文件目录不存在")
        self.__image_paths = list(paths.list_images(image_path))
        self.__labels = []
        self.__data = []
        pass

    def __del__(self):
        pass

    def start_describe(self, save_path):
        for (i, image_path) in enumerate(self.__image_paths):
            image = cv.imread(image_path)
            label = image_path.split(os.path.sep)[-1].split(".")[0]
            features = image_to_feature_vector(image)
            self.__data.append(features)
            self.__labels.append(label)

            if i > 0 and i % 1000 == 0:
                CONSOLE.info("处理 {} / {}".format(i, len(self.__image_paths)))

        le = LabelEncoder()
        self.__labels = le.fit_transform(self.__labels)
        self.__data = np.array(self.__data) / 255.0
        self.__labels = np_utils.to_categorical(self.__labels, 2)
        CONSOLE.info("开始构建训练与测试数据集")
        train_data, test_data, train_labels, test_labels = train_test_split(self.__data, self.__labels,
                                                                            test_size=0.25, random_state=42)
        model = Sequential()
        model.add(Dense(768, input_dim=3072, init="uniform", activation="relu"))
        model.add(Dense(384, activation="relu", kernel_initializer="uniform"))
        model.add(Dense(2))
        model.add(Activation("softmax"))

        CONSOLE.info("编译模型")
        sgd = SGD(lr=0.01)
        model.compile(loss="binary_crossentropy", optimizer=sgd, metrics=["accuracy"])
        model.fit(train_data, train_labels, epochs=50, batch_size=128, verbose=1)
        CONSOLE.info("评估测试数据集")
        loss, accuracy = model.evaluate(test_data, test_labels, batch_size=128, verbose=1)
        CONSOLE.info("loss={:.4f}, accuracy: {:.4f}%".format(loss, accuracy * 100))
        CONSOLE.info("将数据与权重文件输出到文件")
        model.save(save_path)
