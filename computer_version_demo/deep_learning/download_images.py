#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse

if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-u", "--url", required=True, help="包含图像URL的文件的路径")
    ap.add_argument("-o", "--output", required=True, help="图像输出目录的路径")
    args = vars(ap.parse_args())
