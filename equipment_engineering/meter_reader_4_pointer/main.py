#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import abc
from abc import ABC
import argparse
import os


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
                log("设置模式 ...")
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
                log("调试模式 ...")
                start_with_debug()
            except Exception as e:
                log(e, ERROR)
        else:
            self.next.run(request)


class RunVisionMode(EquipmentRunner):

    def run(self, request):
        if True is request["windows"]:
            try:
                log("可视化模式 ...")
                start_with_vision()
            except Exception as e:
                log(e, ERROR)


class RunBackendMode(EquipmentRunner):

    def run(self, request):
        if True is request["backend"]:
            try:
                log("后台模式 ...")
                start_with_backend()
            except Exception as e:
                log(e, ERROR)
        else:
            self.next.run(request)


def fork():
    setting_mode = RunSettingMode()
    debug_mode = RunDebugMode()
    vision_mode = RunVisionMode()
    backend_mode = RunBackendMode()

    setting_mode.next = debug_mode
    debug_mode.next = backend_mode
    backend_mode.next = vision_mode
    # try:
    #     os.chdir("/tmp")
    #     os.setsid()
    #     os.umask(0)
    setting_mode.run(args)
    # except OSError:
    #     pass


if "__main__" == __name__:
    from reader_4_pointer import start_with_vision, start_with_debug, set_detector_argument, start_with_backend
    from reader_4_pointer import version, log, ERROR, input_number_check

    version()
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--debug", type=bool, help=" debug模式", default=False)
    ap.add_argument("-s", "--set", type=bool, help="设置模式", default=False)
    ap.add_argument("-w", "--windows", type=bool, help="可视化模式", default=True)
    ap.add_argument("-b", "--backend", type=bool, help="后台模式", default=False)
    ap.add_argument("-p", "--path", help="日志存放位置")
    args = vars(ap.parse_args())
    fork()
