#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
import cv2 as cv
import imutils
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import logging
import numpy as np


logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)8s][%(filename)s][%(levelname)s] - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
CONSOLE = logging.getLogger("dev")
CONSOLE.setLevel(logging.DEBUG)


def pre_process(path_of_image):
    image = cv.imread(path_of_image)
    orig = image.copy()
    image = cv.resize(image, (28, 28))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    # 添加额外的尺寸
    # 使用CNN在批训练/分类图像, 假设通道最后j进行排序，则通过np.expand_dims
    # 向数组添加额外的尺寸可以使图像具有形状（1，宽度，高度，3）
    image = np.expand_dims(image, axis=0)
    CONSOLE.info("加载网络模型")
    return image, orig


if "__main__" == __name__:
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--model", required=True, help="训练后的模型")
    ap.add_argument("-i", "--image", required=True, help="输入检测图像")
    args = vars(ap.parse_args())
    data, input_image = pre_process(args["image"])
    CONSOLE.info("加载模型")
    model = load_model(args["model"])
    notNazha, nazha = model.predict(data)[0]
    label = "nazha" if nazha > notNazha else "Not Nazha"
    proba = nazha if nazha > notNazha else notNazha
    content = "{}: {:.2f}%".format(label, proba * 100)
    output = imutils.resize(input_image, width=400)
    cv.putText(output, content, (10, 25), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv.imshow("Output", output)
    cv.waitKey(0)
    cv.destroyAllWindows()
