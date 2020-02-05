#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import os
import numpy as np

"""

"""


def get_hog_descriptor(image):
    hog = cv.HOGDescriptor()
    h, w = image.shape[:2]
    rate = 64 / w
    image = cv.resize(image, (64, np.int(rate * h)))
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    bg = np.zeros((128, 64), dtype=np.uint8)
    bg[:, :] = 127
    h, w = gray.shape
    dy = (128 - h) // 2
    bg[dy:h + dy, :] = gray
    cv.imshow("hog_bg", bg)
    cv.waitKey(0)
    fv = hog.compute(bg, winStride=(8, 8), padding=(0, 0))
    return fv


def main():
    image = cv.imread("../../../raspberry-auto/pic/box_04.bmp")
    hog_desc = get_hog_descriptor(image)
    print(len(hog_desc))
    one_fv = np.zeros([len(hog_desc)], dtype=np.float32)
    for i in range(len(hog_desc)):
        one_fv[i] = hog_desc[i][0]
    one_fv = np.reshape(one_fv, [-1, len(hog_desc)])
    print(len(one_fv), len(one_fv[0]))
    svm = cv.ml.SVM_load('svm_data.dat')
    result = svm.predict(one_fv)[1]
    print(result)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
