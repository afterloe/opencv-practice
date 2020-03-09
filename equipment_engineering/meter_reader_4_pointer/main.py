#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from sample import logger
from sample import argument_set
import argparse

if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--debug", type=bool, help="开启可视化窗口， 进入debug模式", default=False)
    ap.add_argument("-s", "--set", type=bool, help="进入设置模式", default=False)
    ap.add_argument("-w", "--windows", type=bool, help="开启窗口模式", default=True)
    args = vars(ap.parse_args())
    if True is args["set"]:
        logger("进入参数设置模式...")
        argument_set()