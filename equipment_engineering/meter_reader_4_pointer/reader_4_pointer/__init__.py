#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from .argument_helper import ArgumentHelper
from .logger import *
import os

ARGUMENT_HELPER = ArgumentHelper()


def version():
    log("指针式仪表识别软件 v1.2")


def debug():
    pass


def input_number_check(key):
    try:
        value = input("输入%s: " % key)
        if False is value.isnumeric():
            assert Exception(key)
        return int(value)
    except:
        log("%s必须为数字！" % key, ERROR)
        os.exit(101)


def set_detector_argument(min_angle, max_angle, min_value, max_value):
    try:
        if False is min_angle.isnumeric():
            assert Exception("表盘最小值对应的刻度")
        if False is max_angle.isnumeric():
            assert Exception("表盘最大值对应的刻度")
        if False is min_value.isnumeric():
            assert Exception("表盘最小值")
        if False is max_value.isnumeric():
            assert Exception("表盘最大值")
        min_angle = int(min_angle)
        max_angle = int(max_angle)
        min_value = int(min_value)
        max_value = int(max_value)
        ARGUMENT_HELPER.setArgument(min_angle, max_angle, min_value, max_value)
    except Exception as e:
        log("%s 必须为数字！" % e, ERROR)
        os.exit(101)
