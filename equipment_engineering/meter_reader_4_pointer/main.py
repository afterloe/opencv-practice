#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import abc
import argparse
from abc import ABC

"""

"""


class EquipmentRunner:

    def __init__(self):
        self.__successor = None

    def setNext(self, successor):
        self.__successor = successor
        return self.__successor

    @abc.abstractmethod
    def run(self, request):
        pass


class RunSettingMode(EquipmentRunner, ABC):

    __args = None

    def __init__(self) -> None:
        super().__init__()

    def run(self, request):
        if True is request["set"]:
            try:
                log("进入参数设置模式...")
                min_angle = input_number_check("表盘最小值对应的刻度")
                max_angle = input_number_check("表盘最大值对应的刻度")
                min_value = input_number_check("表盘最小值")
                max_value = input_number_check("表盘最大值")
                set_detector_argument(min_angle, max_angle, min_value, max_value)
            except Exception as e:
                log(e, ERROR)
        else:
            return "Next"


if "__main__" == __name__:
    from reader_4_pointer import *

    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--debug", type=bool, help="开启可视化窗口， 进入debug模式", default=False)
    ap.add_argument("-s", "--set", type=bool, help="进入设置模式", default=False)
    ap.add_argument("-w", "--windows", type=bool, help="开启窗口模式", default=True)
    args = vars(ap.parse_args())

    runner = EquipmentRunner()
    setting_mode = RunSettingMode()
    runner.setNext(setting_mode)
    runner.run(args)
