#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import classification_report
from shallownet import ShallowNet
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.datasets import cifar10
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import logging


__version__ = "1.0.0"

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
CONSOLE = logging.getLogger("dev")
CONSOLE.setLevel(logging.DEBUG)
CONSOLE.info("cifar10类对象练习 %s", __version__)


if "__main__" == __name__:
    CONSOLE.info("加载CIFAR-10数据集")
    (train_x, train_y), (test_x, test_y) = cifar10.load_data()
    train_x = train_x.astype("float") / 255.0
    test_x = test_x.astype("float") / 255.0
    lb = LabelBinarizer()
    train_y = lb.fit_transform(train_y)
    test_y = lb.transform(test_y)
    label_names = ["airplane", "automobile", "bird", "cat", "deer",
                   "dog", "frog", "horse", "ship", "truck"]
    CONSOLE.info("编译模型")
    opt = SGD(lr=0.01)
    model = ShallowNet.build(32, 32, 3, 10)
    model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])
    CONSOLE.info("训练模型")
    H = model.fit(train_x, train_y, validation_data=(test_x, test_y), batch_size=32, epochs=100, verbose=1)
    CONSOLE.info("评估模型")
    predictions = model.predict(test_x, batch_size=100)
    CONSOLE.info("输出分类结果报告")
    print(classification_report(test_y.argmax(axis=1), predictions.argmax(axis=1), target_names=label_names))
    CONSOLE.info("绘制折线图")
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
