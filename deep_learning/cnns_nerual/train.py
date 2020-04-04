#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import matplotlib

from keras.preprocessing.image import img_to_array, ImageDataGenerator
from keras.optimizers import Adam
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from smallervggnet import SmallerVGGNet
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

# 初始化训练的时期数，初始学习率，
# ＃批次大小和训练图像尺寸
EPOCHS = 100  # 训练的时期数, 即训练次数
INIT_LR = 1e-3  # 初始学习速率，值1e-3是Adam优化器的默认值
BS = 32  # 每个时期有多个批次, 批量图像传递到网络中进行训练
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
        # 提取 图像标签 -> eg: dataset/{CLASS_LABEL}/{FILENAME}.jpg
        label = image_path.split(os.path.sep)[-2]
        LABELS.append(label)
    DATA = np.array(DATA, dtype="float") / 255.0  # 归一化
    LABELS = np.array(LABELS)
    CONSOLE.info("数据矩阵: {:.2f} Mb".format(DATA.nbytes / (1024 * 1000.0)))
    return DATA, LABELS


def run_train(DATA, LABEL):
    # 输入一组类别标签（即代数据集中人类可读的类别标签的字符串）。
    # 将类标签转换为一键编码的向量, 并从Keras CNN进行整数类标签预测，然后将其转换回人类可读的标签。
    lb = LabelBinarizer()
    LABELS = lb.fit_transform(LABEL)
    # 用于创建训练和测试分组的偏移量, 使用80％的数据划分为训练, 其余20％用于测试
    train_x, test_x, train_y, test_y = train_test_split(DATA, LABELS, test_size=0.2, random_state=42)
    # 用于数据增强，该技术用于获取数据集中的现有图像并应用随机变换（旋转，剪切等）以生成其他训练数据。数据扩充有助于防止过度拟合。
    # 由于使用的数据点数量有限（每个类少于250张图像）, 需要在训练过程中利用数据增强功能为模型提供更多图像（基于现有图像）进行训练
    aug = ImageDataGenerator(rotation_range=25, width_shift_range=0.1, height_shift_range=0.1, shear_range=0.2,
                             zoom_range=0.2, horizontal_flip=True, fill_mode="nearest")
    CONSOLE.info("模型初始化")
    model = SmallerVGGNet.build(width=IMAGE_DIMS[1], height=IMAGE_DIMS[0], channel=IMAGE_DIMS[2],
                                classes=len(lb.classes_))
    # Adam优化器，用于训练网络的优化器的常用方法。
    opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
    model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])
    CONSOLE.info("启动训练")
    H = model.fit_generator(aug.flow(train_x, train_y, batch_size=BS),
                            validation_data=(test_x, test_y),
                            steps_per_epoch=len(train_x) // BS,
                            # use_multiprocessing=True,  # 使用GPU进行运算
                            epochs=EPOCHS, verbose=1)
    # 每个类别 500-1,000张图像以获得更好的识别效果
    CONSOLE.info("模型训练完毕")
    return model, lb, H


def destructor(MODEL, BINARY, mode_path, binary_path) -> None:
    CONSOLE.info("模型序列化")
    MODEL.save(mode_path)
    CONSOLE.info("二进制文件序列化")
    file = open(binary_path, "wb")
    file.write(pickle.dumps(BINARY))
    file.close()


def draw_plt(H, png_path) -> None:
    # 将plt生成的图像进行本地保存
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
