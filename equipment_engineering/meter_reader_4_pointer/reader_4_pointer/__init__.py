#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from .argument_helper import ArgumentHelper
from .debug_helper import DebugHelper
from .logger import *
import os

ARGUMENT_HELPER = ArgumentHelper()


def version():
    log("指针式仪表识别软件 v1.2")


def input_number_check(key):
    try:
        value = input("输入%s: " % key)
        if False is value.isnumeric():
            assert Exception(key)
        return int(value)
    except:
        log("%s必须为数字！" % key, ERROR)
        os._exit(101)


def set_detector_argument(min_angle, max_angle, min_value, max_value):
    try:
        min_angle = int(min_angle)
        max_angle = int(max_angle)
        min_value = int(min_value)
        max_value = int(max_value)
        ARGUMENT_HELPER.setArgument(min_angle, max_angle, min_value, max_value)
    except Exception as e:
        log("%s必须为数字！" % e, ERROR)
        os._exit(101)


def start_with_debug():
    # try:
        debug = DebugHelper(ARGUMENT_HELPER.getArgument())
        debug.calibrate_gauge()
    # except Exception as e:
    #     log(e, ERROR)
    #     os._exit(102)