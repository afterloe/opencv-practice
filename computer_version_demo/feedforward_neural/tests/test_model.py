#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
from imutils import paths
from keras.models import load_model
import logging
import numpy as np
from ..sample.funs import image_to_feature_vector
import unittest

CLASSES = ["cat", "dog"]
MODEL_PATH = "G:/Project/py3/computer_version_demo/feedforward_neural/out/simple_neural_network.hdf5"
TEST_IMAGES_PATH = "G:/Project/py3/computer_version_demo/feedforward_neural/resources"

logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S')
console = logging.getLogger("dev")
console.setLevel(logging.DEBUG)


class TestModel(unittest.TestCase):

    def setUp(self) -> None:
        console.info("加载前馈网络模型和权重文件: %s" % MODEL_PATH)
        self.__model = load_model(MODEL_PATH)
        console.info("加载测试图像集: %s" % TEST_IMAGES_PATH)
        self.__image_list = paths.list_images(TEST_IMAGES_PATH)
        pass

    def test_detector(self):
        for image_path in self.__image_list:
            console.info("图像分类: %s" % image_path[image_path.rfind("/") + 1:])
            image = cv.imread(image_path)
            features = image_to_feature_vector(image) / 255.0
            features = np.array([features])
            probs = self.__model.predict(features)[0]
            prediction = probs.argmax(axis=0)
            content = "{}: {:.2f}%".format(CLASSES[prediction], probs[prediction] * 100)
            cv.putText(image, content, (10, 35), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 3)
            console.info("%s is %s" % (image_path, content))
            cv.imshow("image", image)
            cv.waitKey(0)


if "__main__" == __name__:
    unittest.main()
