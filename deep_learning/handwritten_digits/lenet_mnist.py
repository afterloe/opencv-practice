#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import logging
from src.lenet import LeNet
from tensorflow.keras.optimizers import SGD
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.utils import check_random_state
from keras.utils import np_utils
from keras.datasets import mnist
from sklearn import datasets
from tensorflow.keras import backend as K
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

__version__ = "1.0.0"

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
CONSOLE = logging.getLogger("dev")
CONSOLE.setLevel(logging.DEBUG)
CONSOLE.info("LeNet使用 %s", __version__)

if "__main__" == __name__:
    CONSOLE.info("访问MNIST ... ...")
    (trainData, trainLabels), (testData, testLabels) = mnist.load_data()
    # X, y = datasets.fetch_openml('mnist_784', version=1, return_X_y=True)
    # X = X.astype(np.float32)
    # X /= 255.0
    # X -= X.mean(axis=0)
    # train_data, train_label, test_data, test_label = train_test_split(X, y, test_size=0.25, random_state=42)
    le = LabelBinarizer()
    trainLabels = le.fit_transform(trainLabels)
    testLabels = le.fit_transform(testLabels)
    if K.image_data_format() == "channels_first":
        trainData = trainData.reshape((trainData.shape[0], 1, 28, 28))
        testData = testData.reshape((testData.shape[0], 1, 28, 28))
    # otherwise, we are using "channels last" ordering, so the design
    # matrix shape should be: num_samples x rows x columns x depth
    else:
        trainData = trainData.reshape((trainData.shape[0], 28, 28, 1))
        testData = testData.reshape((testData.shape[0], 28, 28, 1))
    # scale data to the range of [0, 1]
    trainData = trainData.astype("float32") / 255.0
    testData = testData.astype("float32") / 255.0
    # trainLabels = np_utils.to_categorical(trainLabels, 10)
    # testLabels = np_utils.to_categorical(testLabels, 10)

    CONSOLE.info("编译模型")
    opt = SGD(lr=0.01)
    model = LeNet.build(28, 28, 1, 10)
    model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

    CONSOLE.info("模型训练")
    H = model.fit(trainData, trainLabels, validation_data=(testData, testLabels), batch_size=128,
                  epochs=60, verbose=1)
    CONSOLE.info("网络评估")
    predictions = model.predict(testData, batch_size=128)
    CONSOLE.info("输出评估报告")
    print(classification_report(testLabels.argmax(axis=1), predictions.argmax(axis=1),
                                target_names=[str(x) for x in le.classes_]))

    CONSOLE.info("输出训练路线图")
    matplotlib.use("Agg")
    plt.style.use("ggplot")
    plt.figure()
    plt.plot(np.arange(0, 100), H.history["loss"], label="train_loss")
    plt.plot(np.arange(0, 100), H.history["val_loss"], label="val_loss")
    plt.plot(np.arange(0, 100), H.history["accuracy"], label="train_accuracy")
    plt.plot(np.arange(0, 100), H.history["val_accuracy"], label="val_accuracy")
    plt.title("Training Loss and Accuracy")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss / Accuracy")
    plt.legend()
    plt.savefig("./plt.png")