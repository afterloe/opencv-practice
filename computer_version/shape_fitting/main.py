#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
from sample import ShapeFitting

if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="输入需要拟合的图像")
    args = vars(ap.parse_args())
    shape_fitting = ShapeFitting(args["image"])
    shape_fitting.run()
