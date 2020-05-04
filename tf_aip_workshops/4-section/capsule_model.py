#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import tensorflow as tf
from tensorflow.keras.layers import Conv2D
import numpy as np


class CapsuleNetModel(object):
    def __init__(self, batch_size, n_classes, iter_routing):
        self.__batch_size = batch_size
        self.__n_classes = n_classes
        self.__iter_routing = iter_routing

    def CapsuleNet(self, image):
        with tf.variable_creator_scope("Conv1_layer") as scope:
            output = Conv2D(image, num_outputs=256, kernel_size=[9, 9], strides=1, padding="VALID", scope=scope)
            assert [self.__batch_size, 20, 20, 256] == output.get_shape()
        with tf.variable_creator_scope("PrimaryCaps_layer") as scope:
            pass
        pass
