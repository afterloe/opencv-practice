#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import os
import tensorflow as tf

"""
Tensor 相关变换
    -	数据类型变换 tf.cast
    -	维度变换 tf.reshape
    -	数据顺序变换 tr.reverse
"""


def main():
    c1 = tf.constant([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], dtype=tf.float32, name="c1")
    print(c1)
    c2 = tf.cast(c1, dtype=tf.int32)
    print(c2)

    r1 = tf.random.uniform(shape=[90000], minval=0.0, maxval=255.0, dtype=tf.float32, name="r1")
    # r2 = 90000 = 300 * 300
    r2 = tf.reshape(r1, [300, 300], name="r2")
    r3 = tf.cast(r2, dtype=tf.uint8)
    cv.imshow("300* 300", r3.numpy())
    cv.waitKey(0)
    r4 = tf.random.normal(shape=[256, 256], mean=50, stddev=20, dtype=tf.float32, name="r4")
    r5 = tf.reshape(r4, [-1])
    print(r5)

    v1 = tf.constant([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=tf.float32, name="v1")
    # tf.reverse(tensor,axis, name=None)
    # axis - 要反转的维度的索引, 必须是以下类型之一：int32、int64,
    v2 = tf.reverse(v1, [0])
    v3 = tf.reverse(v1, [0, 1])
    v4 = tf.reverse(v1, [1])
    print(v1.numpy())  # 1, 2, 3, 4, 5, 6, 7, 8, 9
    print(v2.numpy())  # 7, 8, 9, 4, 5, 6, 1, 2, 3
    print(v3.numpy())  # 9, 8, 7, 6, 5, 4, 3, 2, 1
    print(v4.numpy())  # 3, 2, 1, 6, 5, 4, 9, 8, 7


if "__main__" == __name__:
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    main()
    cv.destroyAllWindows()
