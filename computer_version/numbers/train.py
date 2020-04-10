#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import os
import numpy as np
# import imutils
# from PIL import Image

"""

"""

images = []
labels = []
path_of_train = "./train_data"
classifier = "./svm_number.data"


def load_data():
    files = os.listdir(path_of_train)
    count = len(files)
    sample_data = np.zeros((count, 28 * 48), dtype=np.float32)
    index = 0
    for file_name in files:
        file_path = os.path.join(path_of_train, file_name)
        if True is os.path.isfile(file_path):
            images.append(file_path)
            labels.append(file_name[:1])
            img = cv.imread(file_path, cv.IMREAD_GRAYSCALE)
            img = cv.resize(img, (28, 48))
            row = np.reshape(img, (-1, 28 * 48))
            sample_data[index] = row
            index += 1
    return sample_data, np.asarray(labels, np.int32)


def test_train(data):
    svm = cv.ml.SVM_load(classifier)
    result = svm.predict(data)[1]
    print("[info]: {}".format(result))


def main():
    train_data, train_labels = load_data()
    svm = cv.ml.SVM_create()
    svm.setKernel(cv.ml.SVM_LINEAR)
    svm.setType(cv.ml.SVM_C_SVC)
    svm.setC(2.67)
    svm.setGamma(5.383)
    svm.train(train_data, cv.ml.ROW_SAMPLE, train_labels)
    svm.save(classifier)
    print("[info]: 分类完成")
    test_train(train_data)


if "__main__" == __name__:
    main()
