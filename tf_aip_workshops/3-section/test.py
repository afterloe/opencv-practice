#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
import numpy as np
from PIL import Image
import tensorflow as tf
from nets.nasnet import nasnet
from matplotlib import pyplot as plt
import logging
import os

model_clazz = __import__("model")
slim = tf.contrib.slim

image_size = nasnet.build_nasnet_mobile.default_image_size  # 224


def check_accuracy(sess):
    sess.run(model.test_init_op)
    num_correct, num_samples = 0, 0
    i = 0
    while True:
        i += 1
        CONSOLE.info(i)
        try:
            correct_prediction, accuracy, logits = sess.run([model.correct_prediction, model.accuracy, model.logits])
            num_correct += correct_prediction.sum()
            num_samples += correct_prediction.shape[0]
            CONSOLE.info("accuracy {} {}".format(accuracy, logits))
        except tf.errors.OutOfRangeError:
            CONSOLE.info("over")
            break
        acc = float(num_correct) / num_samples
        return acc


def check_digital(image_dir, sess):
    image = Image.open(image_dir)
    if "RGB" != image.mode:
        image = image.convert("RGB")
    image = np.asarray(image.resize((image_size, image_size)), dtype=np.float32).reshape(1, image_size, image_size, 3)
    image = 2 * (image / 255.0) - 1.0
    prediction = sess.run(model.logits, {model.images: image})
    # CONSOLE.info(prediction)
    pre = prediction.argmax()
    CONSOLE.info(pre)
    content = ""
    if 1 == pre:
        content = "cat"
    elif 2 == pre:
        content = "dog"
    elif 3 == pre:
        content = "panda"
    plt.imshow(np.asarray((image[0] + 1) * 255 / 2, np.uint8))
    plt.show()
    CONSOLE.info("%s -- %s" % (content, image_dir))
    return pre


if "__main__" == __name__:
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S')
    CONSOLE = logging.getLogger("dev")
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dir", required=True, type=str, help="检测训练集")
    ap.add_argument("-e", "--eval-dir", required=True, type=str, help="测试数据集")
    ap.add_argument("-s", "--batch-size", default=32, type=int, help="批处理次数")
    args = vars(ap.parse_args())
    model = model_clazz.CustomizeNASNetModel()
    model.build_model("test", test_data_dir=args["eval_dir"], batch_size=args["batch_size"])
    with tf.Session() as session:
        model.load_cpk(model.global_step, session, 1, model.saver, model.save_path)
        val_acc = check_accuracy(session)
        CONSOLE.info("val accuracy: %f" % val_acc)
        img_dir = "/mount/data/afterloe resources/12485.jpg"
        check_digital(img_dir, session)
        CONSOLE.info("--------------------------------")
        img_dir = os.path.sep.join([args["dir"], "cat", "cat.27.jpg"])
        check_digital(img_dir, session)
        CONSOLE.info("--------------------------------")
        img_dir = os.path.sep.join([args["dir"], "dog", "dog.93.jpg"])
        check_digital(img_dir, session)
        CONSOLE.info("--------------------------------")
        img_dir = os.path.sep.join([args["dir"], "panda", "00000005.jpg"])
        check_digital(img_dir, session)
        CONSOLE.info("--------------------------------")
