#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os
import io
import pandas as pd
import tensorflow as tf
import logging

from PIL import Image  # python3 install pillow
from object_detection.utils import dataset_util
from collections import namedtuple

__version__ = "1.0.0"

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
CONSOLE = logging.getLogger("dev")
CONSOLE.setLevel(logging.DEBUG)
CONSOLE.info("csv to record %s", __version__)


flags = tf.app.flags
flags.DEFINE_string("csv_input", "", "Path to the CSV input")
flags.DEFINE_string("output_path", "", "Path to output TFRecord")
flags.DEFINE_string("label", "", "Name of class label")
flags.DEFINE_string("image_path", "", "path to images")
FLAGS = flags.FLAGS


def class_text_to_int(row_label):
    if row_label == '1':
        return 1
    else:
        return -1


def split(df, group):
    data = namedtuple("data", ["filename", "object"])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path):
    with tf.gfile.GFile(os.path.join(path, str(group.filename)), "rb") as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size
    filename = group.filename.encode("utf8")
    image_format = b"jpg"
    xmins, xmaxs, ymins, ymaxs, classes_text, classes = [], [], [], [], [], []
    for index, row in group.object.iterrows():
        xmins.append(row["xmin"] / width)
        xmaxs.append(row["xmax"] / width)
        ymins.append(row["ymin"] / height)
        ymaxs.append(row["ymax"] / height)
        classes_text.append(str(row["class"]).encode("utf8"))
        classes.append(class_text_to_int(row["class"]))
    return tf.train.Example(features=tf.train.Features(feature={
        "image/height": dataset_util.int64_feature(height),
        "image/width": dataset_util.int64_feature(width),
        "image/filename": dataset_util.bytes_feature(filename),
        "image/source_id": dataset_util.bytes_feature(filename),
        "image/encoded": dataset_util.bytes_feature(encoded_jpg),
        "image/format": dataset_util.bytes_feature(image_format),
        "image/object/bbox/xmin": dataset_util.float_list_feature(xmins),
        "image/object/bbox/xmax": dataset_util.float_list_feature(xmaxs),
        "image/object/bbox/ymin": dataset_util.float_list_feature(ymins),
        "image/object/bbox/ymax": dataset_util.float_list_feature(ymaxs),
        "image/object/class/text": dataset_util.bytes_list_feature(classes_text),
        "image/object/class/label": dataset_util.int64_list_feature(classes),
    }))


def main(_):
    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)
    path = os.path.join(os.getcwd(), FLAGS.image_path)
    example = pd.read_csv(FLAGS.csv_input)
    grouped = split(example, "filename")
    for group in grouped:
        tf_example = create_tf_example(group, path)
        writer.write(tf_example.SerializeToString())
    writer.close()
    output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    CONSOLE.info("Successfully created the TFRecords: %s" % output_path)


if "__main__" == __name__:
    tf.app.run()
