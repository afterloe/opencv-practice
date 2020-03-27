#!/usr/bin/env python3
# -*- coding=utf-8 -*-


from keras.models import Sequential
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Activation, Flatten, Dropout, Dense
from keras import backend as K


class SmallerVGGNet(object):

    @staticmethod
    def build(width, height, channel, classes):
        # 初始化模型以及输入形状
        model = Sequential()
        input_shape = (height, width, channel)
        chan_dim = -1
        if "channels_first" == K.image_data_format():
            input_shape = (channel, height, width)
            chan_dim = 1

        # CONV => RELU => POOL
        # 输入层 32个 个3*3 卷积核
        model.add(Conv2D(32, (3, 3), padding="same", input_shape=input_shape))
        # 使用 RELU 激活功能，然后进行批量归一化
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chan_dim))
        model.add(MaxPooling2D(pool_size=(3, 3)))
        model.add(Dropout(0.25))

        # (CONV => RELU) * 2 => POOL
        # 将多个CONV和RELU层堆叠在一起, 将过滤器尺寸从32增加到64。在网络中越深入，体积的空间尺寸就越小。
        # 将最大合并大小从3x3减少到2x2
        model.add(Conv2D(64, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chan_dim))
        model.add(Conv2D(64, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chan_dim))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        # another (CONV => RELU) * 2 => POOL
        # 将此处的过滤器大小增加到128个。并将执行25％的节点进行删除操作
        model.add(Conv2D(128, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chan_dim))
        model.add(Conv2D(128, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chan_dim))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        # FC => RELU
        # 完全连接层由 Dense（1024）指定，并具有校正的线性单元激活函数和批处理归一化功能。
        model.add(Flatten())
        model.add(Dense(1024))
        model.add(Activation("relu"))
        model.add(BatchNormalization())
        # 删除操作最后一次执行, 训练期间删除了50％的节点
        model.add(Dropout(0.5))
        model.add(Dense(classes))
        # 使用softmax分类器对模型进行完善
        model.add(Activation("softmax"))

        return model
