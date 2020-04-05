#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""

svm.train(Sample, Layout, Responses)
 - Sample: 训练样本数据/HOG特征数据
 - Layout: 有两种组织方式ml.ROW_SAMPLE、ml.COL_SAMPLE
 - Response: 每个输入样本的标签
"""


class TrainUtil(object):

    def __init__(self):
        pass

    @staticmethod
    def svm_run(model, data_set, args):
        svm = cv.ml.SVM_create()
        svm.setKernel(cv.ml.SVM_LINEAR)
        svm.setType(cv.ml.SVM_C_SVC)
        svm.setC(2.67)
        svm.setGamma(5.383)
        train_data, response = data_set(**args)
        response = np.reshape(response, [-1, 1])
        svm.train(train_data, cv.ml.ROW_SAMPLE, response)
        svm.save(model)

    @staticmethod
    def verification(image, model):
        origin = cv.resize(image.copy(), (0, 0), fx=0.2, fy=0.2)
        gray = cv.cvtColor(origin, cv.COLOR_BGR2GRAY)
        h, w = origin.shape[: 2]
        svm = cv.ml.SVM_load(model)
        sum_x = 0
        sum_y = 0
        count = 0
        hog = cv.HOGDescriptor()
        for row in range(64, h - 64, 4):
            for col in range(32, w - 32, 4):
                win_roi = gray[row - 64: row + 64, col - 32: col + 32]
                hog_desc = hog.compute(win_roi, winStride=(8, 8), padding=(0, 0))
                one_fv = np.zeros([len(hog_desc)], dtype=np.float32)
                for i in range(len(hog_desc)):
                    one_fv[i] = hog_desc[i][0]
                one_fv = one_fv.reshape(-1, len(hog_desc))
                result = svm.predict(one_fv)[1]
                if 0 < result[0][0]:
                    sum_x += col - 32
                    sum_y += row - 64
                    count += 1
                    cv.rectangle(origin, (col - 32, row - 64), (col + 32, row + 64), (0, 233, 255), 1, cv.LINE_AA)
        x = sum_x // count
        y = sum_y // count
        cv.rectangle(origin, (x, y), (x + 64, y + 128), (0, 0, 255), 2, cv.LINE_AA)
