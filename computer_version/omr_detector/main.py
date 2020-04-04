#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
from sample.omr_util import OMRUtil


"""
        光标阅读（OMR即是“Optical Mark Reader”），是用光学扫描的方法来识别按一定格式印刷或书写的标记，并将其转换为计算机能接受的电信号的程序.
简而言之，光学标记识别对统一人类标记形式和考试进行评分和解释的有着巨大的市场。

主要步骤如下:
    1. 图像检测 (OMRUtil.detector)
            1.1 对图像进行滤波和边缘检测，提取纸张轮廓，并对轮廓进行排序
            1.2 对纸张疑似轮廓，进行矩形拟合，并通过四点变换提取纸张的疑似鸟瞰图
    2. OMR推断 (OMRUtil.infer)
            2.1 对OMR区域进行轮廓检索和排序
            2.2 遍历排序结果，对每行OMR区域进行像素值检测
            2.3 根据预设好的答案进行匹配
            2.4 输出推断结果
"""
if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="omr 的图像")
    args = vars(ap.parse_args())
    omr_util = OMRUtil(args["image"])
    paper = omr_util.detector()
    omr_util.infer(paper)
