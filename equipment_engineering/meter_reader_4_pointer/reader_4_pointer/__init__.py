#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from argument_setter import ArgumentSetter
from log import
import argparse


if "__main__" == __name__:
    core.log("指针式仪表识别软件 v1.2")
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--debug", type=bool, help="开启可视化窗口， 进入debug模式", default=False)
    ap.add_argument("-s", "--set", type=bool, help="进入设置模式", default=False)
    ap.add_argument("-w", "--windows", type=bool, help="开启窗口模式", default=True)
    args = vars(ap.parse_args())
    setter = core.ArgumentSetter()
    if True is args["set"]:
        logging.log("进入参数设置模式...")
        setter.setArgument()
