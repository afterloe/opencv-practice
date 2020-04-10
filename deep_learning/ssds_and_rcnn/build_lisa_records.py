#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from .config import lisa_config as config
from .utils.tfannotation import TFAnnotation
from sklearn.model_selection import train_test_split
from PIL import Image
import tensorflow as tf
import os


def main():
    # 将配置文件输出到文件上
    f = open(config.CLASSES_FILE, "w")
    for (key, value) in config.CLASSES.items():
        item = ("item{\n"
                "\tid: " + str(value) + "\n"
                "\tname: '" + key + "'\n"
                "}\n")
        f.write(item)
    f.close()
    D = {}
    rows = open(config.ANNOTATION_PATH).read().strip().split("\n")
    for row in rows[1:]:
        row = row.split(",")[0].split(";")
        image_path = label, start_x, start_y, end_x, end_y, _ = row
        start_x, start_y = float(start_x), float(start_y)
        end_x, end_y = float(end_x), float(end_y)

        if label not in config.CLASSES:
            continue
        p = os.path.sep.join([config.BASE_PATH, image_path])
        b = D.get(p, [])
        b.append((label, start_x, start_y, end_x, end_y))
        D[p] = b
    train_keys, test_keys = train_test_split(list(D.keys()), test_size=config.TEST_SIZE, random_state=42)
    datasets = [
        ("train", train_keys, config.TRAIN_RECORD),
        ("test", test_keys, config.TEST_RECORD)
    ]
    for (d_type, keys, output_path) in datasets:
        print("[INFO] processing '{}' ...".format(d_type))
        writer = tf.python_io.TFRecordWriter(output_path)
        total = 0
        for key in keys:
            encoded = tf.gfile.GFile(k, "rb").read()
            encoded = bytes(encoded)
            pil_image = Image.open(key)
            w, h = pil_image.size[:2]
            filename = key.split(os.path.sep)[-1]
            encoding = filename[filename.rfind(".") + 1:]
            tf_annotation = TFAnnotation()
            tf_annotation.image = encoded
            tf_annotation.encoding = encoding
            tf_annotation.filename = filename
            tf_annotation.width = w
            tf_annotation.height = h
            for (label, (start_x, start_y, end_x, end_y)) in D[key]:
                x_min = start_x / w
                x_max = end_x / w
                y_min = start_y / h
                y_max = end_y / h
                tf_annotation.x_mins.append(x_min)
                tf_annotation.x_maxs.append(x_max)
                tf_annotation.y_mins.append(y_min)
                tf_annotation.y_maxs.append(y_max)
                tf_annotation.text_labels.append(label.encode("utf8"))
                tf_annotation.classes.append(config.CLASSES[label])
                tf_annotation.difficult.append(0)
                total += 1
            features = tf.train.Feature(feature=tf_annotation.build())
            example = tf.train.Example(features=features)
            writer.write(example.SerializeToString())
    writer.close()
    print("[INFO] {} examples saved for '{}'".format(total, d_type))


if "__main__" == __name__:
    tf.app.run()
