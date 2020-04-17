#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
import tensorflow as tf
import sys
from nets.nasnet import nasnet
from preprocessing import preprocessing_factory
from imutils.paths import list_images
import os
import logging

slim = tf.contrib.slim
__version__ = "1.0.0"
image = nasnet.build_nasnet_mobile.defautlt_image_size

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
CONSOLE = logging.getLogger("dev")
CONSOLE.setLevel(logging.DEBUG)
CONSOLE.info("将图像转换为dataset %s" % __version__)


def get_images_list(directory):
    labels = os.listdir(directory)
    labels.sort()
    files_and_labels = []
    for label in labels:
        images = list_images(os.path.sep.join([directory, label]))
        files_and_labels.append((*images, label))
    file_names, labels = zip(*files_and_labels)
    file_names = list(file_names)
    labels = list(labels)
    unique_labels = list(set(labels))
    label_to_int = {}
    for i, label in enumerate(sorted(unique_labels)):
        label_to_int[label] = i + 1
        CONSOLE.info(label, label_to_int[label])
    labels = [label_to_int[l] for l in labels]
    CONSOLE.info(labels[:6])
    CONSOLE.info(labels[-6:])
    return file_names, labels


if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dir", required=True, help="图像目录", type=str)
    args = vars(ap)
    fn, l = get_images_list(args["dir"])
    CONSOLE.info(fn)
    CONSOLE.info(l)
