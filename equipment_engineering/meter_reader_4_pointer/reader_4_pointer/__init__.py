#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
from .argument_helper import ArgumentHelper
from .logger import log


if "__main__" == __name__:
    log("指针式仪表识别软件 v1.2")
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--debug", type=bool, help="开启可视化窗口， 进入debug模式", default=False)
    ap.add_argument("-s", "--set", type=bool, help="进入设置模式", default=False)
    ap.add_argument("-w", "--windows", type=bool, help="开启窗口模式", default=True)
    args = vars(ap.parse_args())
    setter = ArgumentHelper()
    if True is args["set"]:
        log("进入参数设置模式...")
        min_angle = input("输入表盘最小值对应的刻度: ")
        max_angle = input("输入表盘最大值对应的刻度: ")
        min_value = input("输入表盘最小值: ")
        max_value = input("输入表盘最大值: ")
        setter.setArgument(min_angle, max_angle, min_value, max_value)
