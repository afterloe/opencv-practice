#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
from sample.scan import ScanRunner


if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="文档图像扫描")
    args = vars(ap.parse_args())
    scan = ScanRunner(args["image"])
    scan.run()
