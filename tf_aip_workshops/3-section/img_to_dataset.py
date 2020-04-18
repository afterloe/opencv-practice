#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import tensorflow as tf
from nets.nasnet import nasnet
from preprocessing import preprocessing_factory
from imutils.paths import list_images
import os
import logging

slim = tf.contrib.slim


num_workers = 8
image_size = nasnet.build_nasnet_mobile.default_image_size  # 224
image_pre_processing_fn = preprocessing_factory.get_preprocessing("nasnet_mobile", is_training=True)
image_eval_pre_processing_fn = preprocessing_factory.get_preprocessing("nasnet_mobile", is_training=False)

CONSOLE = logging.getLogger("dev")


def get_images_list(directory):
    labels = os.listdir(directory)
    labels.sort()
    files_and_labels = []
    for label in labels:
        images = list_images(os.path.sep.join([directory, label]))
        for i in images:
            files_and_labels.append((i, label))
    file_names, labels = zip(*files_and_labels)
    file_names = list(file_names)
    labels = list(labels)
    unique_labels = list(set(labels))
    label_to_int = {}
    for i, label in enumerate(sorted(unique_labels)):
        label_to_int[label] = i + 1
    labels = [label_to_int[l] for l in labels]
    return file_names, labels


def parse_function(filename, label):
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
