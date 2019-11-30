#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2
import imutils
import argparse
import numpy as np


def initArg():
    ap = argparse.ArgumentParser()
    ap.description = "image to process by afterloe version is 1.0.0"
    ap.add_argument("-h", "-help", help="启动参数")
    ap.add_argument("-i", "-image", help="Image to process")
    ap.add_argument("-p", "-pattern", help="Image light pattern to apply to image input")
    ap.add_argument("-l", "-lightMethod", default=1, type=int,
                    help="Method to remove backgroun light, 0 differenec, 1 div, 2 no light removal")
    ap.add_argument("-s", "-segMethod", default=1, type=int,
                    help="Method to segment: 1 connected Components, 2 connectec components with stats, 3 find Contours")
    return vars(ap.parse_args())


def removeLight(image, pattern, method=1):  # method: 1 - 采用加法移； 2 - 采用减法移除
    if 1 == method:
        image32 = image.convertTo(cv2.CV_32F)  # 将图片转换为 32位 浮点数
        pattern32 = pattern.convertTo(cv2.CV_32F)
        aux = 1 - (image32 / pattern32)  # 对矩阵进行数学运算，将图像除以模式并反转结果
        aux = aux.convertTo(cv2.CV_8U, 255)  # 再将结果转换为8位深度的图像， 并用alpha参数将图像从0放大到255
    else:
        aux = pattern - image
    return aux


def calculateLightPattern(image):  # 光模式或背景近似结果
    return cv2.blur(image, (image.cols / 3, image.cols / 3), 0)


def connectedComponents(image):  # 连通组件定义绘制过程
    num_objects, labels = cv2.connectedComponents(image)
    if 2 > num_objects:
        print("No objects detected")
        return
    else:
        print("Number of objects detected: %d" % (num_objects - 1))
    output = np.zeros(image.rows, image.cols, cv2.CV_8UC3)
    rng = np.random.RandomState(0xFFFFFFFF)
    i = 0
    while i < num_objects:
        i += 1
        mask = output.setTo

argMap = initArg()
FILE = "G:/pic/1yuan.jpg"
image = cv2.imread(FILE, cv2.IMREAD_COLOR)
cv2.imshow("before", imutils.resize(image, 640, 320))
image_noise = cv2.medianBlur(image, 5)  # 消除噪声
# python中的 三元表达式的解决方案
img_thr = cv2.threshold(image, 30, 255, cv2.THRESH_BINARY) if 2 != argMap["l"] else cv2.threshold(image, 140, 255,
                                                                                                  cv2.THRESH_BINARY_INV)

cv2.imshow("after", imutils.resize(image_noise, 640, 329))
cv2.waitKey(0)
cv2.destroyAllWindows()
