#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
from sample.object_tract import ObjectTract

if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", required=True, help="输入检测图像")
    ap.add_argument("-b", "--buffer", type=int, default=64, help="最大缓冲区大小")
    args = vars(ap.parse_args())
    tractUtil = ObjectTract(video=args["video"], max_buff=args["buffer"])
    tractUtil.start_track()
