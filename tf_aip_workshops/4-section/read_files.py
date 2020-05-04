#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
from tensorflow.keras.datasets.fashion_mnist import load_data
import logging


if "__main__" == __name__:
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S')
    CONSOLE = logging.getLogger("dev")
    # ~/.keras/datasets/fashion-mnist
    (train_images, train_labels), (test_images, test_labels) = load_data()
    CONSOLE.info("输入数据: {}".format(train_images[1]))
    CONSOLE.info("输入数据形状: {}".format(train_images.shape))
    CONSOLE.info("输入数据的标签: {}".format(train_labels))
    cv.imshow("image-1", train_images[1].reshape(-1, 28))
    cv.waitKey(0)
    cv.destroyAllWindows()
