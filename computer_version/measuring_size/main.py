#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
from sample.measure import Measure

if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="检测的图像")
    ap.add_argument("-w", "--width", type=float, required=True, help="图像中最左边对象的宽度（厘米）")
    args = vars(ap.parse_args())
    measure_util = Measure(args["image"])
    measure_util.set_width(args["width"])
    measure_util.measure_by_object()

