#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
from reader_4_pointer import *

"""

"""


def setting_model():
    try:
        log("进入参数设置模式...")
        min_angle = input_number_check("表盘最小值对应的刻度")
        max_angle = input_number_check("表盘最大值对应的刻度")
        min_value = input_number_check("表盘最小值")
        max_value = input_number_check("表盘最大值")
        set_detector_argument(min_angle, max_angle, min_value, max_value)
    except Exception as e:
        log(e, ERROR)


if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--debug", type=bool, help="开启可视化窗口， 进入debug模式", default=False)
    ap.add_argument("-s", "--set", type=bool, help="进入设置模式", default=False)
    ap.add_argument("-w", "--windows", type=bool, help="开启窗口模式", default=True)
    args = vars(ap.parse_args())
    if True is args["set"]:
        setting_model()
