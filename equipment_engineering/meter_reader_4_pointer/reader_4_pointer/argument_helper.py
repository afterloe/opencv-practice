#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os
from .logger import *
import yaml


DEFAULT_CONFIG_SAVE_PATH = "../config.yml"
CHARACTER = "utf-8"


class ArgumentHelper:
    __min_angle = 0
    __max_angle = 0
    __min_value = 0
    __max_value = 0

    def __init__(self):
        flag = os.path.isfile(DEFAULT_CONFIG_SAVE_PATH)
        if False is flag:
            log("%s 文件不存在， 无法读取配置" % DEFAULT_CONFIG_SAVE_PATH)
            log("按照默认配置进行")
            return
        with open(DEFAULT_CONFIG_SAVE_PATH, "r", encoding=CHARACTER) as f:
            config = yaml.load(f.read(), Loader=yaml.SafeLoader)
            self.__min_angle = config["min_angle"]
            self.__max_angle = config["max_angle"]
            self.__min_value = config["min_value"]
            self.__max_value = config["max_value"]
            log("读取配置文件 %s" % DEFAULT_CONFIG_SAVE_PATH, SUCCESS)
            log("表盘最小值对应的刻度: %s" % self.__min_angle)
            log("表盘最大值对应的刻度: %s" % self.__max_angle)
            log("表盘最小值: %s" % self.__min_value)
            log("表盘最大值: %s" % self.__max_value)

    def setArgument(self, min_angle, max_angle, min_value, max_value):
        # self.__min_angle = input("输入表盘最小值对应的刻度: ")
        # self.__max_angle = input("输入表盘最大值对应的刻度: ")
        # self.__min_value = input("输入表盘最小值: ")
        # self.__max_value = input("输入表盘最大值: ")
        self.__min_angle = min_angle
        self.__max_angle = max_angle
        self.__min_value = min_value
        self.__max_value = max_value
        caps = {
            "min_angle": self.__min_angle,
            "max_angle": self.__max_angle,
            "min_value": self.__min_value,
            "max_value": self.__max_value
        }

        with open(DEFAULT_CONFIG_SAVE_PATH, "w", encoding=CHARACTER) as f:
            yaml.dump(caps, f, Dumper=yaml.SafeDumper)
            log("配置已写入 %s" % DEFAULT_CONFIG_SAVE_PATH, SUCCESS)
            log("表盘最小值对应的刻度: %s" % self.__min_angle)
            log("表盘最大值对应的刻度: %s" % self.__max_angle)
            log("表盘最小值: %s" % self.__min_value)
            log("表盘最大值: %s" % self.__max_value)

    def getArgument(self):
        return self.__min_angle, self.__max_angle, self.__min_value, self.__max_value

