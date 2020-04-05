#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os

# 将BASE_PATH定义为LISA交通标志目录
BASE_PATH = "lisa"

# 使用BASE_PATH 导出LISA随附的注释文件的路径
ANNOTATION_PATH = os.path.sep.join([BASE_PATH, "allAnnotations.csv"])
TRAIN_RECORD = os.path.sep.join([BASE_PATH, "records", "training.record"])
TEST_RECORD = os.path.sep.join([BASE_PATH, "records", "classes.pbtxt"])
TEST_SIZE = 0.25  # 设置路径集， 25%的测试数据， 75%用于训练数据
CLASSES = {"pedestrianCrossing": 1, "signalAhead": 2, "stop": 3}

