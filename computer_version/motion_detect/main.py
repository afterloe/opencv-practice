#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
from sample.object_tract import ObjectTract

if "__main__" == __name__:
    # 移动对象轨迹绘制与跟踪， 使用颜色跟踪
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="输入检测视频")
    ap.add_argument("-b", "--buffer", type=int, default=64, help="最大缓冲区大小")
    args = vars(ap.parse_args())
    tractUtil = ObjectTract(args.get("video", False), max_buff=args["buffer"])
    tractUtil.start_track()
