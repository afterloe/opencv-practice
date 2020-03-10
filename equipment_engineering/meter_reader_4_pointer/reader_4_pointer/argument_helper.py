#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os
from .logger import *
import yaml


DEFAULT_CONFIG_SAVE_PATH = "../config.yml"
CHARACTER = "utf-8"


class ArgumentHelper:
    _min_angle = 0
    _max_angle = 0
    _min_value = 0
    _max_value = 0

    def __init__(self):
        flag = os.path.isfile(DEFAULT_CONFIG_SAVE_PATH)
        if False is flag:
            log("%s 文件不存在，无法读取配置，按照默认配置进行" % DEFAULT_CONFIG_SAVE_PATH)
            return
        with open(DEFAULT_CONFIG_SAVE_PATH, "r", encoding=CHARACTER) as f:
            config = yaml.load(f.read(), Loader=yaml.SafeLoader)
            self._min_angle = config["min_angle"]
            self._max_angle = config["max_angle"]
            self._min_value = config["min_value"]
            self._max_value = config["max_value"]
            log("读取配置文件 %s" % DEFAULT_CONFIG_SAVE_PATH, SUCCESS)
            log("表盘最小值对应的刻度: %s" % self._min_angle)
            log("表盘最大值对应的刻度: %s" % self._max_angle)
            log("表盘最小值: %s" % self._min_value)
            log("表盘最大值: %s" % self._max_value)

    def setArgument(self, min_angle, max_angle, min_value, max_value):
        self._min_angle = min_angle
        self._max_angle = max_angle
        self._min_value = min_value
        self._max_value = max_value
        caps = {
            "min_angle": self._min_angle,
            "max_angle": self._max_angle,
            "min_value": self._min_value,
            "max_value": self._max_value
        }

        with open(DEFAULT_CONFIG_SAVE_PATH, "w", encoding=CHARACTER) as f:
            yaml.dump(caps, f, Dumper=yaml.SafeDumper)
            log("配置已写入 %s" % DEFAULT_CONFIG_SAVE_PATH, SUCCESS)
            log("表盘最小值对应的刻度: %s" % self._min_angle)
            log("表盘最大值对应的刻度: %s" % self._max_angle)
            log("表盘最小值: %s" % self._min_value)
            log("表盘最大值: %s" % self._max_value)

    def getArgument(self):
        return self._min_angle, self._max_angle, self._min_value, self._max_value

