#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from tensorflow.keras.layers import Conv2D, MaxPooling2D, Activation, Flatten, Dense, BatchNormalization, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.regularizers import l2
from tensorflow.keras import backend as K


class CONVNetFactory(object):

    def __init__(self):
        pass

    @staticmethod
    def build(name, *args, **kargs):
        """
            VGGNet, GoogLeNet, ResNet, SqueezeNet

        :param name:
        :param args:
        :param kargs:
        :return:
        """
        mappings = {
            "shallownet": CONVNetFactory.ShallowNet,
            "lenet": CONVNetFactory.LeNet,
            "alexnet": CONVNetFactory.AlexNet,
            # "karpathynet": ConvNetFactory.KarpathyNet,
            "minivggnet": CONVNetFactory.MiniVGGNet
        }
        builder = mappings.get(name, None)
        return builder(*args, **kargs)

    @staticmethod
    def AlexNet(channels, height, width, classes, **kwargs):
        # kwargs = {reg=0.0002}
        model = Sequential()
        input_shape = (height, width, channels)
        chan_dim = -1
        if "channels_first" == K.image_data_format:
            input_shape = (channels, height, width)
            chan_dim = 1

        # CONV => RELU = > POOL
        # CONV 96个卷积，大小11 * 11, 启动步长为 4 * 4, 并使用L2 权重正则化参数
        model.add(Conv2D(96, (11, 11), strides=(4, 4), input_shape=input_shape, padding="same",
                         kernel_regularizer=l2(kwargs["reg"])))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chan_dim))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
        model.add(Dropout(0.25))  # 用25%的拟合

        # CONV => RELU => POOL
        model.add(Conv2D(256, (5, 5), padding="same", kernel_regularizer=l2(kwargs["reg"])))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chan_dim))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
        model.add(Dropout(0.25))

        # 学习更深、更丰富的特性，叠加了多个 CONV => RELU 的POOL操作
        # 前两个CONV滤波器学习384，3×3滤波器，而第三个CONV学习256，3×3滤波器。
        # 再次，将多个CONV =>RELU层堆叠到POOL层使我们的网络能够学习更丰富、更有潜力的特性
        model.add(Conv2D(384, (3, 3), padding="same", kernel_regularizer=l2(kwargs["reg"])))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chan_dim))
        model.add(Conv2D(384, (3, 3), padding="same", kernel_regularizer=l2(kwargs["reg"])))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chan_dim))
        model.add(Conv2D(256, (3, 3), padding="same", kernel_regularizer=l2(kwargs["reg"])))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chan_dim))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
        model.add(Dropout(0.25))

        # Block #4: first set of FC => RELU layers
        # 多维表示分解成一个标准的前馈
        # 使用两个完全连接层的网络(每个4096个节点)
        model.add(Flatten())
        model.add(Dense(4096, kernel_regularizer=l2(kwargs["reg"])))
        model.add(Activation("relu"))
        model.add(BatchNormalization())
        model.add(Dropout(0.5))

        #  Block #5: second set of FC => RELU layers
        model.add(Dense(4096, kernel_regularizer=l2(kwargs["reg"])))
        model.add(Activation("relu"))
        model.add(BatchNormalization())
        model.add(Dropout(0.5))

        # softmax classifier
        model.add(Dense(classes, kernel_regularizer=l2(kwargs["reg"])))
        model.add(Activation("softmax"))
        return model

    @staticmethod
    def MiniVGGNet(channels, height, width, classes, **kwargs):
        model = Sequential()
        input_shape = (height, width, channels)
        chan_dim = -1
        if "channels_first" == K.image_data_format:
            input_shape = (channels, height, width)
            chan_dim = 1

        model.add(Conv2D(32, (3, 3), padding="same", input_shape=input_shape))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chan_dim))
        model.add(Conv2D(32, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chan_dim))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(64, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chan_dim))
        model.add(Conv2D(64, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chan_dim))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Flatten())
        model.add(Dense(512))
        model.add(Activation("relu"))
        model.add(BatchNormalization())
        model.add(Dropout(0.5))

        model.add(Dense(classes))
        model.add(Activation("softmax"))
        return model

    @staticmethod
    def LeNet(channels, height, width, classes, **kwargs):
        model = Sequential()
        input_shape = (height, width, channels)
        if "channels_first" == K.image_data_format:
            input_shape = (channels, height, width)
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
        model.add(Activation("softmax"))

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
