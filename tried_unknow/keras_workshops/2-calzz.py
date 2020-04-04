#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import tensorflow as tf
import os
import cv2 as cv
import numpy as np

"""
tensor 张量

零维的张量可以看成是标量(Scalar)
一维的张量可以看成是向量(vector)
二维的张量可以看成是矩阵或者数据平面
三维的张量可以看成是数据立方体

常见的张量创建方法有如下：
    用常量函数创建张量
    用zero/ones函数创建张量
    用fill函数来创建张量
    用linspace函数来创建张量
    用随机函数创建随机张量
"""


def main():
    # 创建常量类型的tensor
    c1 = tf.constant("learning TensorFlow", dtype=tf.string, name="c1")  # 零维
    c2 = tf.constant([1, 2, 3], dtype=tf.int32, name="c2")  # 一维
    c3 = tf.constant([[1, 2, 3], [4, 5, 6]], dtype=tf.int32, name="c3")  # 二维
    print(c1)
    print(c1.numpy())
    print("----------------------------------------")
    print(c2)
    print(c2.numpy())
    print("----------------------------------------")
    print(c3)
    print(c3.numpy())
    print("----------------------------------------")

    # 创建带有默认值的tensor
    z1 = tf.zeros(shape=[3], dtype=tf.float32, name="z1")
    z2 = tf.ones(shape=[4, 4, 4], dtype=tf.int32, name="z2")
    print(z1)
    print("----------------------------------------")
    print(z2)
    print("----------------------------------------")

    # 创建线性空间， 注意要有 .
    # start, stop, num, name
    t1 = tf.linspace(10., 100., 22, name="t1")
    print(t1)
    print("----------------------------------------")

    # 随机函数创建tensor
    r1 = tf.random.uniform([256, 256], minval=0.0, maxval=255.0, dtype=tf.float32, name="r1")
    # shape, mean, stddev, dtype, seed,
    r2 = tf.random.normal([100], mean=50, stddev=10.0, dtype=tf.float32, name="r2")
    result = r1.numpy()
    cv.imshow("result", np.uint8(result))
    cv.waitKey(0)
    print(r2.numpy())


if "__main__" == __name__:
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    main()
    cv.destroyAllWindows()
