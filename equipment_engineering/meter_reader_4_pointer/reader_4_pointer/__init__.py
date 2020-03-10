#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from .argument_helper import ArgumentHelper
from .current_util import is_number
from .debug_helper import DebugHelper
from .logger import *
import os

ARGUMENT_HELPER = ArgumentHelper()

__version__ = '1.3'


def version():
    log("指针式仪表识别软件 v%s" % __version__)


def input_number_check(key):
    value = input("输入%s: " % key)
    if False is is_number(value):
        log("%s必须为数字！" % key, ERROR)
        os._exit(101)
    return value


def set_detector_argument(min_angle, max_angle, min_value, max_value, util):
    try:
        ARGUMENT_HELPER.setArgument(min_angle, max_angle, min_value, max_value, util)
    except Exception as e:
        log("%s必须为数字！" % e, ERROR)
        os._exit(101)


def start_with_debug():
    try:
        debug = DebugHelper(ARGUMENT_HELPER.getArgument())
        debug.calibrate_gauge()
    except Exception as e:
        log(e, ERROR)
        os._exit(102)