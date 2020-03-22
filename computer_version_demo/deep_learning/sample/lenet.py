#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.models import Sequential
from keras.layers.core import Activation, Flatten, Dense
from keras import backend as K


# 卷积神经网络
# LeNet是一个小型卷积神经网络
class LeNet(object):

    @staticmethod
    def build(width, height, channel, classes):
        model = Sequential()
        input_shape = (height, width, channel)
        if "channels_first" == K.image_data_format():
            input_shape = (channel, height, width)
        # CONV => RELU => POOL
        # CONV层设置20个卷积核，每个大小为5×5。应用ReLU激活函数，然后在x和y方向上以2的步幅进行2×2的最大池化
        model.add(Conv2D(20, (5, 5), padding="same", input_shape=input_shape))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

        # 第二个 CONV => RELU => POOL
        model.add(Conv2D(50, (5, 5), padding="same"))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

        # 全连接层 FLATT => DENSE => RELU => SOFTMAX
        # 获取前面的MaxPooling2D层的输出并将其展平为单个向量。此操作可以应用密集/完全连接的层。
        # 全连接层包含500个节点，使用另一个非线性ReLU激活。
        model.add(Flatten())
        model.add(Dense(500))
        model.add(Activation("relu"))

        # 定义了一个完全连接的层，节点数等于类数（即我们要识别的分类）。 然后将此密集层输入到softmax分类器中
        # 将为每个分类产生概率。
        model.add(Dense(classes))
        model.add(Activation("softmax"))  # softmax 执行分类器
        return model
