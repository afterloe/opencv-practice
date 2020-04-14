#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import tensorflow as tf

"""
TensorFlow - hello world

使用安装的TensorFlow 2.0并导入
"""


def main():
    # 导入数据集, 数据集下载地址为: http://yann.lecun.com/exdb/mnist/
    mnist = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    # 将整数数据集转换为浮点数
    x_train, x_test = x_train / 255.0, x_test / 255.0
    # 搭建Sequential模型，并将数据堆叠起来
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    # 训练
    model.fit(x_train, y_train, epochs=5)
    # 验证
    model.evaluate(x_test, y_test)


if "__main__" == __name__:
    main()
