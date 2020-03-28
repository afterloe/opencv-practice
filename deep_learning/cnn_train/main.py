#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
import logging
from preprocessor import SimpleDatasetLoader, SimplePreprocessor, ImageToArrayPreprocessor
from shallownet import ShallowNet
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from tensorflow.keras.optimizers import SGD
from imutils import paths
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


__version__ = "1.0.0"

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
CONSOLE = logging.getLogger("dev")
CONSOLE.setLevel(logging.DEBUG)
CONSOLE.info("第一cnn练习 %s", __version__)


if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dataset", required=True, help="数据存储路径")
    # ap.add_argument("-k", "--neighbors", type=int, default=1, help="分类的最近相近点")
    # ap.add_argument("-j", "--jobs", type=int, default=1, help="KNN算法的作业数")
    args = vars(ap.parse_args())
    #  (1)从磁盘加载图像，(2)将它的大小调整为32×32像素，
    #  (3)对通道尺寸进行排序 (4)输出图像。
    sp = SimplePreprocessor(32, 32)
    iap = ImageToArrayPreprocessor()
    sdl = SimpleDatasetLoader(preprocessor=[sp, iap])
    image_paths = list(paths.list_images(args["dataset"]))
    data, labels = sdl.load(image_paths=image_paths, verbose=500)
    data = data.astype("float") / 255.0
    train_x, test_x, train_y, test_y = train_test_split(data, labels, test_size=0.25, random_state=42)
    train_y = LabelBinarizer().fit_transform(train_y)
    test_y = LabelBinarizer().fit_transform(test_y)
    CONSOLE.info("编译模型")
    opt = SGD(lr=0.005)
    model = ShallowNet.build(32, 32, 3, 3)
    model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])
    CONSOLE.info("训练模型")
    H = model.fit(train_x, train_y, validation_data=(test_x, test_y), batch_size=32, epochs=100, verbose=1)
    CONSOLE.info("评估模型")
    predictions = model.predict(test_x, batch_size=32)
    CONSOLE.info("输出分类结果")
    print(classification_report(test_y.argmax(axis=1), predictions.argmax(axis=1),
                                target_names=["cat", "dog", "panda"]))
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
