#!/usr/bin/env python3
# -*- coding=utf-8 -*-

#import cv2 as cv
import os
import tensorflow as tf

"""

"""


def main():
    x = tf.random.uniform([3, 3])

    print("Is there a GPU available: "),
    print(tf.config.experimental.list_physical_devices())

    print("Is the Tensor on GPU #0:  "),
    print(x.device.endswith('GPU:0'))

    # with tf.device("/GPU:0"):
    #     v4 = tf.Variable(tf.random.normal([2, 2], mean=0, stddev=4, dtype=tf.float32), name="v4")
    #     init = tf.global_variables_initializer()
    #     sess = tf.Session(graph=tf.get_default_graph())
    #     sess.run(init)
    #     print(sess.run(v4))
    pass


if "__main__" == __name__:
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    main()
