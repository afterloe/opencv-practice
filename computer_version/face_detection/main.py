#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
from sample import FaceDetection

if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="检测图片地址")
    ap.add_argument("-p", "--prototxt", required=True, help="Caffe模型描述文件")
    ap.add_argument("-m", "--model", required=True, help="Caffe模型文件")
    ap.add_argument("-c", "--confidence", type=float, default=0.5, help="检测阈值")
    args = vars(ap.parse_args())
    detector = FaceDetection(args["model"], args["prototxt"])
    detector.setConfidence(args["confidence"])
    detector.loadImage(args["image"])
    detector.inference()
