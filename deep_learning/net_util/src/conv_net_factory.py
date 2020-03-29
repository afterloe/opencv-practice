#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from tensorflow.keras.layers import Conv2D, MaxPooling2D, Activation, Flatten, Dropout, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras import backend as K


class ConvNetFactory(object):

    def __init__(self):
        pass

    @staticmethod
    def build(name, *args, **kargs):
        mappings = {
            "shallownet": ConvNetFactory.ShallowNet
            # "lenet": ConvNetFactory.LeNet,
            # "karpathynet": ConvNetFactory.KarpathyNet,
            # "minivggnet": ConvNetFactory.MiniVGGNet
        }
        builder = mappings.get(name, None)
        return builder(*args, **kargs)

    @staticmethod
    def ShallowNet(channels, height, width, classes, **kwargs):
        model = Sequential()
        input_shape = (height, width, channels)
        if "channels_first" == K.image_data_format():
            input_shape = (channels, height, width)
        # define the first (and only) CONV => RELU layer
        model.add(Conv2D(32, (3, 3), padding="same", input_shape=input_shape))
        model.add(Activation("relu"))

        # add a FC layer followed by the soft-max classifier
        model.add(Flatten())
        model.add(Dense(classes))
        model.add(Activation("softmax"))
        return model
