#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
from sample.code import Code
import logging

__version__ = "1.0.1"

if "__main__" == __name__:
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S')
    console = logging.getLogger("dev")
    console.setLevel(logging.DEBUG)
    console.info("simple neural network %s", __version__)
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dataset", required=True, help="数据集路径")
    ap.add_argument("-m", "--model", required=True, help="输出的模型路径")
    args = vars(ap.parse_args())
    console.info("启动图像描述 ... ... ")
    runner = Code(image_path=args["dataset"])
    runner.start_describe(save_path=args["model"])
