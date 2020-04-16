#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os
import logging
import numpy as np
import tensorflow as tf
from tqdm import tqdm
from PIL import Image

__version__ = "1.0.0"

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
CONSOLE = logging.getLogger("dev")
CONSOLE.setLevel(logging.DEBUG)
CONSOLE.info("将文件转换为TFRecord %s" % __version__)


def load_file(path_of_dir):
    CONSOLE.info("从%s加载数据集 " % path_of_dir)
    labels = []
    files = []
    for dir_path, dir_names, file_names in os.walk(path_of_dir):
        labels.append(dir_path.split(os.path.sep)[-1])
        for file_name in file_names:
            files.append(os.path.sep.join([dir_path, file_name]))
    lab = list(sorted(set(labels)))
    return np.asarray(files), np.asarray(lab)


def make_TFRrc(file_list, labels):
    writer = tf.python_io.TFRecordWriter("data.tfrecords")
    for i in tqdm(range(0, len(labels))):
        img = Image.open(file_list[i])
        img = img.resize((256, 256))
        img_raw = img.tobytes()
        example = tf.train.Example(features=tf.train.Features(feature={
            "label": tf.train.Feature(int64_list=tf.train.Int64List(value=[labels[i]])),
            "img_raw": tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw]))
        }))
        writer.write(example.SerializeToString())
    writer.close()


def main():
    files, labels = load_file("/home/afterloe/data/afterloe resources/animal")
    CONSOLE.info(files)
    CONSOLE.info(labels)
    pass


if "__main__" == __name__:
    main()
