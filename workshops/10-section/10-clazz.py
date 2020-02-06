#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import os
import numpy as np

"""
使用SVM分类训练，对HOG提取的正负样本进行训练处理

SVM分类器使用ml包进行创建，创建之后需要进行设置分类器类型、回归距离参数等内容

SVM训练api如下：
cv.ml.statModel.train(samples, layout, responses)
    - samples 训练样本数据/HOG特征数据
    - layout 组织方式 ROW_SAMPLE/ COL_SAMPLE
    - response 每个样本的标签
"""

# 正向样本集
positive_dir = "../../../raspberry-auto/pic/elec_watch/positive/"
# 反向像本集
negative_dir = "../../../raspberry-auto/pic/elec_watch/negative/"


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


def generate_data_set(p_dir, n_dir):
    train_data = []
    labels = []
    for file_name in os.listdir(p_dir):
        img_dir = os.path.join(p_dir, file_name)
        img = cv.imread(img_dir)
        hog_desc = get_hog_descriptor(img)
        one_fv = np.zeros([len(hog_desc)], dtype=np.float32)
        for i in range(len(hog_desc)):
            one_fv[i] = hog_desc[i][0]
        train_data.append(one_fv)
        labels.append(1)

    for file_name in os.listdir(n_dir):
        img_dir = os.path.join(n_dir, file_name)
        img = cv.imread(img_dir)
        hog_desc = get_hog_descriptor(img)
        one_fv = np.zeros([len(hog_desc)], dtype=np.float32)
        for i in range(len(hog_desc)):
            one_fv[i] = hog_desc[i][0]
        train_data.append(one_fv)
        labels.append(-1)

    return np.array(train_data, dtype=np.float32), np.array(labels, dtype=np.int32)


def main():
    # 线性不可分离分类器， 若是线性可分离可选择神经网络ANN模块
    svm = cv.ml.SVM_create()  # 创建SVM分类器
    svm.setKernel(cv.ml.SVM_LINEAR)  # 设置分类器属性， 线性不可分离
    svm.setType(cv.ml.SVM_C_SVC)  # 设置分类器类型
    svm.setC(2.67)  # 设置优化参数， 默认为0
    svm.setGamma(5.383)  # 核函数参数γ的值， 回归分类的零界限，越大越接近，越小越精准
    train_data, responses = generate_data_set(positive_dir, negative_dir)
    # 样本归一化处理
    responses = np.reshape(responses, [-1, 1])
    # SVM分类, 训练API
    svm.train(train_data, cv.ml.ROW_SAMPLE, responses)
    # 存储训练结果
    svm.save('svm_data.dat')


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
