#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
from sample.facial_landmarks import FacialLandmarks
import logging

__version__ = "1.0.1"

if "__main__" == __name__:
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S')
    console = logging.getLogger("dev")
    console.setLevel(logging.INFO)
    console.info("facial landmarks %s", __version__)
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="从视频中解析")
    ap.add_argument("-i", "--image", help="从图片中解析")
    args = vars(ap.parse_args())
    facial_landmarks = FacialLandmarks()
    if args.get("video", False):
        facial_landmarks.detect_by_video(args["video"])
    elif args.get("image", False):
        facial_landmarks.detect_by_image(args["image"])
    console.error("请输入参数! -v / -i")
