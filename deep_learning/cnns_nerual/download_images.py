#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
import cv2 as cv
from imutils.paths import list_images
import logging
import requests
import os

__version__ = "1.0.2"

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
CONSOLE = logging.getLogger("dev")
CONSOLE.setLevel(logging.DEBUG)
CONSOLE.info("crawl image %s", __version__)


class DownloadUtil(object):

    __total = 0

    def __init__(self):
        self.__warehouse = None
        self.__rows = None

    @property
    def urlFile(self):
        return self.__rows

    @urlFile.setter
    def urlFile(self, url_file):
        self.__rows = open(url_file).read().strip().split("\n")

    @property
    def warehouse(self):
        return self.__warehouse

    @warehouse.setter
    def warehouse(self, path_of_save):
        self.__warehouse = path_of_save

    def run(self):
        if None is self.__warehouse:
            CONSOLE.error("请先设置仓库文件地址")
            return
        for url in self.__rows:
            path_of_image = os.path.sep.join([self.__warehouse, "%s.jpg" % str(self.__total).zfill(8)])
            try:
                req = requests.get(url, timeout=60)
                file = open(path_of_image, "wb")
                file.write(req.content)
                file.close()
                CONSOLE.info("下载地址: %s" % path_of_image)
                self.__total += 1
            except IOError:
                CONSOLE.error("%s 下载失败, 自动跳过" % path_of_image)

    def validation(self):
        if None is self.__warehouse:
            CONSOLE.error("请先设置仓库文件地址")
            return
        images = list_images(self.__warehouse)
        count = 0
        for image_path in images:
            delete = False
            try:
                image = cv.imread(image_path)
                if None is image:
                    delete = True
            except all:
                CONSOLE.error("%s 无法解析， 自动删除" % image_path)
                delete = True
            if delete:
                os.remove(image_path)
            count += 1
            if 0 == count % 100:
                CONSOLE.info("%d 项检测完毕" % count)
        CONSOLE.info("共检测 %d 项图像， 检测完毕" % count)

    def __del__(self):
        pass


if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dir", required=True, help="包含图像URL的文件的路径")
    ap.add_argument("-o", "--output", required=True, help="图像输出目录的路径")
    args = vars(ap.parse_args())
    util = DownloadUtil()
    files = os.listdir(args["dir"])
    for file in files:
        label = file.split(".")[0]
        dir_path = os.path.sep.join([args["output"], label])
        if False is os.path.isdir(dir_path):
            os.mkdir(dir_path)
        util.urlFile = os.path.sep.join([args["dir"], file])
        util.warehouse = dir_path
        util.run()
        util.validation()
