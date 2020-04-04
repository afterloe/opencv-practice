#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Flatten, Dense, Conv2D
from tensorflow.keras import backend as K


class ShallowNet(object):

    @staticmethod
    def build(width, height, channel, classes):
        model = Sequential()
        input_shape = (height, width, channel)
        if "channels_first" == K.image_data_format():
            input_shape = (channel, height, width)
        #  INPUT => CONV => RELU => FC
        model.add(Conv2D(32, (3, 3), padding="same", input_shape=input_shape))
        model.add(Activation("relu"))
        model.add(Flatten())
        model.add(Dense(classes))
        model.add(Activation("softmax"))

        return model
