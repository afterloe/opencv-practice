#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import tensorflow as tf
import os

"""
TensorFlow 相关内容可参照官网进行了解

在TensorFlow编程接口中有几个重要的应用层概念
    -	计算图
    -	会话
    -	数据
    -	操作
    
TensorFlow简单的描述就是构建一张计算图，然后执行计算，其中图的节点表示OP操作，边缘代表张量的流动。
"""


def main():
    print(tf.__version__)
    data = tf.constant("hello world")
    print(data.numpy())


if "__main__" == __name__:
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    main()
