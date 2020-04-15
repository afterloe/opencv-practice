#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import tensorflow as tf
from PIL import Image
from matplotlib import pyplot as plt
from nets.nasnet import pnasnet
import numpy as np
from datasets import imagenet
import logging

slim = tf.contrib.slim

__version__ = "1.0.0"

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
CONSOLE = logging.getLogger("dev")
CONSOLE.setLevel(logging.DEBUG)
CONSOLE.info("tensorflow class %s" % __version__)


def main():
    tf.compat.v1.reset_default_graph()
    image_size = pnasnet.build_pnasnet_large.default_image_size
    labels = imagenet.create_readable_names_for_imagenet_labels()
    sample_images = ["/home/afterloe/data/afterloe resources/animal/cat/cat.13.jpg",
                     "/home/afterloe/data/afterloe resources/animal/dog/dog.45.jpg",
                     "/home/afterloe/data/afterloe resources/animal/panda/00000010.jpg"]
    input_images = tf.placeholder(tf.float32, [None, image_size, image_size, 3])
    x1 = 2 * (input_images / 255.0) - 1.0
    arg_scope = pnasnet.pnasnet_large_arg_scope()
    with slim.arg_scope(arg_scope):
        logits, end_points = pnasnet.build_pnasnet_large(x1, num_classes=1001, is_training=False)
        prob = end_points["Predictions"]
        y = tf.argmax(prob, axis=1)
    checkpoint_file = r"/home/afterloe/public/models/pnasnet/model.ckpt"
    saver = tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess, checkpoint_file)

        def preimg(img):
            ch = 3
            if "RGBA" == img.mode:
                ch = 4
            imgnp = np.asarray(img.resize((image_size, image_size)),
                               dtype=np.float32).reshape(image_size, image_size, ch)
            return imgnp[:, :, :3]

        batch_image = [preimg(Image.open(img_filename)) for img_filename in sample_images]
        org_image = [Image.open(image_filename) for image_filename in sample_images]
        yv, img_norm = sess.run([y, x1], feed_dict={input_images: batch_image})
        CONSOLE.info(yv)
        CONSOLE.info(np.shape(yv))

        def showresult(yy, img_norm, img_org):
            plt.figure()
            p1 = plt.subplot(121)
            p2 = plt.subplot(122)
            p1.imshow(img_org)
            p1.axis("off")
            p1.set_title("organization image")
            p2.imshow((img_norm * 255).astype(np.uint8))
            p2.axis("off")
            p2.set_title("input image")

            plt.show()
            CONSOLE.info(yy)
            CONSOLE.info(labels[yy])

        for yy, img_1, img_2 in zip(yv, batch_image, org_image):
            showresult(yy, img_1, img_2)


if "__main__" == __name__:
    main()
