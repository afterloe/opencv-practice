#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import pickle
import imutils
import cv2 as cv
import os
import logging
import sys

__version__ = "1.0.0"

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
CONSOLE = logging.getLogger("dev")
CONSOLE.setLevel(logging.DEBUG)
CONSOLE.info("分类工具 %s", __version__)

LABEL_MAP = {"1": "战斗暴龙兽", "2": "钢铁加鲁鲁", "3": "红莲骑士兽", "4": "奥米加兽", "5": "阿尔法兽", "6": "杰斯兽",
             "7": "神圣天使兽", "8": "哪吒", "9": "罗小黑"}

if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--model", required=True, help="模型文件地址")
    ap.add_argument("-l", "--labelbin", required=True, help="二进制标签文件地址")
    ap.add_argument("-i", "--image", required=True, help="检测图像")
    args = vars(ap.parse_args())

    image = cv.imread(args["image"])
    if None is image:
        CONSOLE.error("图像地址不存在: %s" % args["image"])
        sys.exit(1)
    output = image.copy()
    image = cv.resize(image, (96, 96))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    CONSOLE.info("加载模型")
    model = load_model(args["model"])
    lb = pickle.loads(open(args["labelbin"], "rb").read())

    CONSOLE.info("图像分类预测")
    proba = model.predict(image)[0]
    idx = np.argmax(proba)
    label = lb.classes_[idx]

    filename = args["image"][args["image"].rfind(os.path.sep) + 1:]
    # 正确， 不正确
    correct = "correct" if filename.rfind(label) != -1 else "incorrect"
    content = "{}: {:.2f}% ({})".format(label, proba[idx] * 100, correct)
    output = imutils.resize(output, width=400)
    cv.putText(output, content, (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    CONSOLE.info(LABEL_MAP[str(label)])
    CONSOLE.info(content)
    cv.imshow("output", output)
    cv.waitKey(0)
    cv.destroyAllWindows()
