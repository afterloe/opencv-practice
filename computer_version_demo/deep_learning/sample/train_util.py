#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import logging
import matplotlib
from keras.preprocessing.image import ImageDataGenerator, img_to_array
from keras.optimizers import Adam
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from imutils import paths
from .lenet import LeNet
import matplotlib.pyplot as plt
import numpy as np
import random
import cv2 as cv
import os

CONSOLE = logging.getLogger("dev")
# 将matplotlib后端设置为``Agg''，以便将图保存到磁盘中, 这点在云服务器上需要特别注意
matplotlib.use("Agg")

# 定义训练时的数量，初始学习率和批量大小
EPOCHS = 25
INIT_LR = 1e-3
BS = 32


class TrainLeNet(object):
    __out_dir, __H = None, None

    def __init__(self, path_of_images):
        self.__data = []
        self.__labels = []
        # 获取输入图像文件夹的路径
        self.__path_of_images = sorted(list(paths.list_images(path_of_images)))
        # 对其进行混洗
        random.seed(42)
        random.shuffle(self.__path_of_images)

    def __del__(self):
        pass

    @property
    def outs(self):
        return self.__out_dir

    @outs.setter
    def outs(self, out_dir):
        self.__out_dir = out_dir

    def run(self):
        # pre process, 图像预处理操作
        for image_path in self.__path_of_images:
            image = cv.imread(image_path)
            image = cv.resize(image, (28, 28))
            image = img_to_array(image)  # 将图像转换为数组数据
            self.__data.append(image)
            label = image_path.split(os.path.sep)[-2]  # 标签提取
            label = 1 if label == "nazha" else 0
            self.__labels.append(label)
        self.__data = np.array(self.__data, dtype="float") / 255.0  # 归一化
        # 对数据执行训练/测试拆分, 使用75％的图像进行训练，25％的图像进行测试
        train_x, test_x, train_y, test_y = train_test_split(self.__data, self.__labels, test_size=0.25, random_state=42)
        # 使用一键编码将标签转换为矢量
        train_y = to_categorical(train_y, num_classes=2)
        test_y = to_categorical(test_y, num_classes=2)
        # 构造图像生成器以进行数据增强
        # 该对象在图像数据集上执行随机旋转，平移，翻转，修剪和剪切。
        # 使用较小的数据集，也可以获得较高的结果
        aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1, height_shift_range=0.1,
                                 shear_range=0.2, zoom_range=0.2, horizontal_flip=True, fill_mode="nearest")
        CONSOLE.info("编译模型")
        model = LeNet.build(width=28, height=28, channel=3, classes=2)
        opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
        # 如果是两个以上的分类使用 categorical_crossentropy
        model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])
        CONSOLE.info("训练模型")
        self.__H = model.fit_generator(aug.flow(train_x, train_y, batch_size=BS), validation_data=(test_x, test_y),
                                       steps_per_epoch=len(train_x) // BS, epochs=EPOCHS, verbose=1)
        CONSOLE.info("序列化模型")
        model.save(self.__out_dir)

    def draw_plt(self, path_of_plt):
        plt.style.use("ggplot")
        plt.figure()
        N = EPOCHS
        plt.plot(np.arange(0, N), self.__H.history["loss"], label="train_loss")
        plt.plot(np.arange(0, N), self.__H.history["val_loss"], label="val_loss")
        plt.plot(np.arange(0, N), self.__H.history["accuracy"], label="train_accuracy")
        plt.plot(np.arange(0, N), self.__H.history["val_accuracy"], label="val_accuracy")
        plt.title("Training Loss and Accuracy on Santa/Not Santa")
        plt.xlabel("Epoch #")
        plt.ylabel("Loss/Accuracy")
        plt.legend(loc="lower left")
        plt.savefig(path_of_plt)
