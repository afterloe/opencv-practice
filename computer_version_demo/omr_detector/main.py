#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
from sample.omr_util import OMRUtil


"""
        光标阅读（OMR即是“Optical Mark Reader”），是用光学扫描的方法来识别按一定格式印刷或书写的标记，并将其转换为计算机能接受的电信号的程序
"""
if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="omr 的图像")
    args = vars(ap.parse_args())
    omr_util = OMRUtil(args["image"])
    paper = omr_util.detector()
    omr_util.infer(paper)
