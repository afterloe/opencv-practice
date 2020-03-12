#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import abc
from abc import ABC
import argparse

"""

"""


class EquipmentRunner(ABC):

    def __init__(self):
        self.__successor = None

    @property
    def mode(self):
        if not self.__successor:
            exit(404)
        return self.__successor

    @mode.setter
    def mode(self, successor):
        self.__successor = successor

    @abc.abstractmethod
    def run(self, request): ...


class RunSettingMode(EquipmentRunner):

    def run(self, request):
        if True is request["set"]:
            try:
                log("进入参数设置模式 ...")
                min_angle = input_number_check("表盘最小值对应的刻度")
                max_angle = input_number_check("表盘最大值对应的刻度")
                min_value = input_number_check("表盘最小值")
                max_value = input_number_check("表盘最大值")
                util = input("仪表单位: ")
                set_detector_argument(min_angle, max_angle, min_value, max_value, util)
            except Exception as e:
                log(e, ERROR)
        else:
            self.next.run(request)


class RunDebugMode(EquipmentRunner):

    def run(self, request):
        if True is request["debug"]:
            try:
                log("进入调试模式 ...")
                start_with_debug()
            except Exception as e:
                log(e, ERROR)
        else:
            self.next.run(request)


class RunVisionMode(EquipmentRunner):

    def run(self, request):
        if True is request["windows"]:
            # try:
                log("以可视化模式运行 ...")
                start_with_vision()
            # except Exception as e:
            #     log(e, ERROR)
        else:
            self.next.run(request)


if "__main__" == __name__:
    from reader_4_pointer import start_with_vision, start_with_debug, set_detector_argument
    from reader_4_pointer import version, log, ERROR

    version()
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--debug", type=bool, help="开启可视化窗口， 进入debug模式", default=False)
    ap.add_argument("-s", "--set", type=bool, help="进入设置模式", default=False)
    ap.add_argument("-w", "--windows", type=bool, help="开启窗口模式", default=True)
    args = vars(ap.parse_args())
    setting_mode = RunSettingMode()
    debug_mode = RunDebugMode()
    vision_mode = RunVisionMode()
    setting_mode.next = debug_mode
    debug_mode.next = vision_mode
    setting_mode.run(args)
