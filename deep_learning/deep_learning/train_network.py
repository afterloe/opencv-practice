#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
import logging
from sample.train_util import TrainLeNet


__version__ = "1.0.1"

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
CONSOLE = logging.getLogger("dev")
CONSOLE.setLevel(logging.DEBUG)
CONSOLE.info("模型训练工具 %s", __version__)

if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dataset", required=True, help="图像仓库")
    ap.add_argument("-m", "--model", required=True, help="输出的模型存放位置")
    ap.add_argument("-p", "--plot", type=str, default="plot.png", help="输出精度与损失比直方图")
    args = vars(ap.parse_args())
    tools = TrainLeNet(args["dataset"])
    tools.outs = args["model"]
    tools.run()
    tools.draw_plt(args["plot"])
