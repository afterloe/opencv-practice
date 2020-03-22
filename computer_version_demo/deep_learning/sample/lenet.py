#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.models import Sequential
from keras.layers.core import Activation, Flatten, Dense
from keras import backend as K


class LeNet(object):

    @staticmethod
    def build(width, height, channel, classes):
        model = Sequential()
        input_shape = (height, width, channel)
        if "channels_first" == K.image_data_format():
            input_shape = (channel, height, width)
        model.add(Conv2D(20, (5, 5), padding="same", input_shape=input_shape))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

        model.add(Conv2D(50, (5, 5), padding="same"))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

        model.add(Flatten())
        model.add(Dense(500))
        model.add(Activation("relu"))
        model.add(Dense(classes))
        model.add(Activation("softmax"))  # softmax 执行分类器
        return model
