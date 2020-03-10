#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os
from .logger import *
import yaml


DEFAULT_CONFIG_SAVE_PATH = "../config.yml"
CHARACTER = "utf-8"


class ArgumentHelper:
    _min_angle, _max_angle, _min_value, _max_value = 0, 0, 0, 0
    _util = ""
    _bool = None

    def __init__(self):
        flag = os.path.isfile(DEFAULT_CONFIG_SAVE_PATH)
        if False is flag:
            log("%s 文件不存在，无法读取配置，按照默认配置进行" % DEFAULT_CONFIG_SAVE_PATH)
            self._bool = True
            return
        with open(DEFAULT_CONFIG_SAVE_PATH, "r", encoding=CHARACTER) as f:
            config = yaml.load(f.read(), Loader=yaml.SafeLoader)
            detector_config = config["detector"]
            self._min_angle = detector_config["min_angle"]
            self._max_angle = detector_config["max_angle"]
            self._min_value = detector_config["min_value"]
            self._util = detector_config["util"]
            log("读取配置文件 %s" % DEFAULT_CONFIG_SAVE_PATH, SUCCESS)
            log("表盘最小值对应的刻度: %s" % self._min_angle)
            log("表盘最大值对应的刻度: %s" % self._max_angle)
            log("表盘最小值: %s" % self._min_value)
            log("表盘最大值: %s" % self._max_value)
            log("单位: %s" % self._util)

    def setArgument(self, min_angle, max_angle, min_value, max_value, util):
        self._min_angle, self._max_angle = min_angle, max_angle
        self._min_value, self._max_value = min_value, max_value
        self._util = util
        detector_config = {
            "min_angle": self._min_angle,
            "max_angle": self._max_angle,
            "min_value": self._min_value,
            "max_value": self._max_value,
            "util": self._util
        }
        config = None
        if True is self._bool:
            config = {}
        else:
            with open(DEFAULT_CONFIG_SAVE_PATH, "r", encoding=CHARACTER) as f:
                config = yaml.load(f.read(), Loader=yaml.SafeLoader)
        config["detector"] = detector_config
        with open(DEFAULT_CONFIG_SAVE_PATH, "w", encoding=CHARACTER) as f:
            yaml.dump(config, f, Dumper=yaml.SafeDumper)
            log("配置已写入 %s" % DEFAULT_CONFIG_SAVE_PATH, SUCCESS)
            log("表盘最小值对应的刻度: %s" % self._min_angle)
            log("表盘最大值对应的刻度: %s" % self._max_angle)
            log("表盘最小值: %s" % self._min_value)
            log("表盘最大值: %s" % self._max_value)
            log("单位: %s" % self._util)

    def getArgument(self):
        return self._min_angle, self._max_angle, self._min_value, self._max_value, self._util
