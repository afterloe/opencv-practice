#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import matplotlib

from keras.preprocessing.image import img_to_array, ImageDataGenerator
from keras.optimizers import Adam
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from .smallervggnet import SmallerVGGNet
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import argparse
import random
import pickle
import cv2 as cv
import os
import logging


__version__ = "1.0.5"

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
CONSOLE = logging.getLogger("dev")
CONSOLE.setLevel(logging.DEBUG)
CONSOLE.info("模型训练工具 %s", __version__)

EPOCHS = 100
INIT_LR = 1e-3
BS = 32
IMAGE_DIMS = (96, 96, 3)


def pre_process(str_path):
    CONSOLE.info("加载%s图像, 并启动预处理" % str_path)
    image_paths = sorted(list(paths.list_images(str_path)))
    random.seed(42)
    random.shuffle(image_paths)
    DATA, LABELS = [], []
    for image_path in image_paths:
        image = cv.imread(image_path)
        image = cv.resize(image, (IMAGE_DIMS[1], IMAGE_DIMS[0]))
        image = img_to_array(image)
        DATA.append(image)
        label = image_path.split(os.path.sep)[-2]
        LABELS.append(label)
    DATA = np.array(DATA, dtype="float") / 255.0
    LABELS = np.array(LABELS)
    CONSOLE.info("数据矩阵: %.2f Mb" % DATA.nbytes / (1024 * 1000.0))
    return DATA, LABELS


def run_train(DATA, LABEL):
    lb = LabelBinarizer()
    LABELS = lb.fit_transform(LABEL)
    train_x, test_x, train_y, test_y = train_test_split(DATA, LABELS, test_size=0.2, random_state=42)
    aug = ImageDataGenerator(rotation_range=25, width_shift_range=0.1, height_shift_range=0.1, shear_range=0.2,
                             zoom_range=0.2, horizontal_flip=True, fill_mode="nearest")
    CONSOLE.info("模型初始化")
    model = SmallerVGGNet.build(width=IMAGE_DIMS[1], height=IMAGE_DIMS[0], channel=IMAGE_DIMS[2],
                                classes=len(lb.classes_))
    opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
    model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])
    CONSOLE.info("启动训练")
    H = model.fit_generator(aug.flow(train_x, train_y, batch_size=BS),
                            validation_data=(test_x, test_y),
                            steps_per_epoch=len(train_x) // BS,
                            epochs=EPOCHS, verbose=1)
    CONSOLE.info("模型训练完毕")
    return model, lb, H


def destructor(MODEL, BINARY, mode_path, binary_path) -> None:
    CONSOLE.info("模型序列化")
    MODEL.save(mode_path)
    CONSOLE.info("二进制文件序列化")
    file = open(binary_path, "wb")
    file.write(pickle.dump(BINARY))
    file.close()


def draw_plt(H, png_path) -> None:
    matplotlib.use("Agg")
    plt.style.use("ggplot")
    plt.figure()
    N = EPOCHS
    plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
    plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
    plt.plot(np.arange(0, N), H.history["accuracy"], label="train_accuracy")
    plt.plot(np.arange(0, N), H.history["val_accuracy"], label="val_accuracy")
    plt.title("Training Loss and Accuracy")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss / Accuracy")
    plt.savefig(png_path)


if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dataset", required=True, help="图像集路径")
    ap.add_argument("-m", "--model", required=True, help="模型输出路径")
    ap.add_argument("-l", "--labelbin", required=True, help="标签二进制文件输出路径")
    ap.add_argument("-p", "--plot", type=str, default="plot.png", help="输出训练曲线")
    args = vars(ap.parse_args())
    data, labels = pre_process(args["dataset"])
    m, binary, h = run_train(data, labels)
    destructor(m, binary, args["model"], args["labelbin"])
    draw_plt(h, args["plot"])
