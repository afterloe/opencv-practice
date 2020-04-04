#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np
import os

"""

"""

RESOURCE_PATH = "G:/Project/opencv-ascs-resources/seven-segment-number"
classifier = "./svm_led.data"
images = []
labels = []


def load_data():
    resources = os.listdir(RESOURCE_PATH)
    count = len(resources)
    sample_data = np.zeros((count, 60 * 120), dtype=np.float32)
    index = 0
    for name in resources:
        resource = os.path.join(RESOURCE_PATH, name)
        if True is os.path.isfile(resource):
            images.append(resource)
            labels.append(name[:1])
            image = cv.imread(resource, cv.IMREAD_GRAYSCALE)
            image = cv.resize(image, (60, 120))
            row = np.reshape(image, (-1, 60 * 120))
            sample_data[index] = row
            index += 1
    return sample_data, np.asarray(labels, np.int32)


def test_data(data):
    svm = cv.ml.SVM_load(classifier)
    result = svm.predict(data)[1]
    print("[INFO]: {}".format(result))


def main():
    data, label = load_data()
    svm = cv.ml.SVM_create()
    svm.setKernel(cv.ml.SVM_LINEAR)
    svm.setType(cv.ml.SVM_C_SVC)
    svm.setC(2.67)
    svm.setGamma(5.383)
    svm.train(data, cv.ml.ROW_SAMPLE, label)
    svm.save(classifier)
    print("[INFO]: 数据分类完成")
    test_data(data)


if "__main__" == __name__:
    main()
