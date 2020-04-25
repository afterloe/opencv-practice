#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import tensorflow as tf
from nets.nasnet import nasnet
from preprocessing import preprocessing_factory
from imutils.paths import list_images
import os
import logging

slim = tf.contrib.slim

"""
处理图像数据集
"""

num_workers = 8  # 定义并行处理数据的线程数量
image_size = nasnet.build_nasnet_mobile.default_image_size  # 224
# 图像批预处理
image_pre_processing_fn = preprocessing_factory.get_preprocessing("nasnet_mobile", is_training=True)
image_eval_pre_processing_fn = preprocessing_factory.get_preprocessing("nasnet_mobile", is_training=False)

CONSOLE = logging.getLogger("dev")


def get_images_list(directory):
    """
    获取目录下所有的图片和标签

    :param directory:  目录
    :return:
    """
    labels = os.listdir(directory)  # 获取所有标签
    labels.sort()  # 对标签进行排序，以便训练和验证都采用相同的顺序进行
    files_and_labels = []  # 创建文件标签列表
    for label in labels:
        images = list_images(os.path.sep.join([directory, label]))
        for i in images:
            files_and_labels.append((i, label))
    file_names, labels = zip(*files_and_labels)
    file_names = list(file_names)
    labels = list(labels)
    unique_labels = list(set(labels))
    # 为每个分类打上标签　{"none":0, "cat": 1, "dog": 2, "panda":3}
    label_to_int = {}
    for i, label in enumerate(sorted(unique_labels)):
        label_to_int[label] = i + 1
    labels = [label_to_int[l] for l in labels]
    return file_names, labels


def parse_function(filename, label):
    """
    图像解码函数
    :param filename:
    :param label:
    :return:
    """
    image_string = tf.read_file(filename)
    image = tf.image.decode_jpeg(image_string, channels=3)
    return image, label


def training_pre_process(image, label):
    image = image_pre_processing_fn(image, image_size, image_size)
    return image, label


def val_pre_process(image, label):
    image = image_eval_pre_processing_fn(image, image_size, image_size)
    return image, label


def create_batched_dataset(filenames, labels, batch_size, is_train=True):
    """
    创建带批次的数据集
    :param filenames:
    :param labels:
    :param batch_size:
    :param is_train:
    :return:
    """
    data_set = tf.data.Dataset.from_tensor_slices((filenames, labels))
    data_set = data_set.map(parse_function, num_parallel_calls=num_workers)
    if True is is_train:
        data_set = data_set.shuffle(buffer_size=len(filenames))
        data_set = data_set.map(training_pre_process, num_parallel_calls=num_workers)
    else:
        data_set = data_set.map(val_pre_process, num_parallel_calls=num_workers)
    return data_set.batch(batch_size)


def create_dataset_fromdir(directory, batch_size, is_train=True):
    filenames, labels = get_images_list(directory)
    num_classes = len(labels)
    data_set = create_batched_dataset(filenames, labels, batch_size, is_train)
    return data_set, num_classes
