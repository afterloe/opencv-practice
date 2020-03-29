#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from collections import namedtuple
from skimage.filters import threshold_local
from skimage import segmentation, measure
import imutils
from imutils import perspective
import numpy as np
import cv2 as cv

# 命名元组, 一种易于创建的轻量级对象类型， 类C/Cpp里的 struct, 就是一种简单的class
"""
    success: boolean, 车牌检测和字符分割是否成功
    plate: mat, 检测到的车牌图像
    thresh: mat, 二值化的车牌图像
    candidates: array, 候选字符列表，用于传递给机器学习分类器以进行最终识别
"""
LICENSE_PLATE = namedtuple("LicensePlateRegion", ["success", "plate", "thresh", "candidates"])


class LicensePlateDetector(object):

    def __init__(self, image, minPlateW=60, minPlateH=20, numChars=7, minCharW=40):
        self.__image = image
        self.__min_plate_w = minPlateW
        self.__min_plate_h = minPlateH
        self.__num_chars = numChars
        self.__min_char_w = minCharW

    def detect(self):
        # 检测图像中的车牌
        lp_regions = self.__detect_plates()
        for lp_region in lp_regions:
            # 检查车牌中的字母
            lp = self.__detect_character_candidates(lp_region)
            if lp.success:
                yield lp, lp_region  # # 产生一个牌照对象和边界框的元组

    def __detect_plates(self):
        return []

    def __detect_character_candidates(self, region):
        plate = perspective.four_point_transform(self.__image, region)
        cv.imshow("perspective transform", imutils.resize(plate, width=400))
        V = cv.split(cv.cvtColor(plate, cv.COLOR_BGR2HSV))[2]
        T = threshold_local(V, 29, offset=15, method="gaussian")
        thresh = (V > T).astype("uint8") * 255
        thresh = cv.bitwise_not(thresh)
        plate = imutils.resize(plate, width=400)
        thresh = imutils.resize(thresh, width=400)
        cv.imshow("Thresh", thresh)
        labels = measure.label(thresh, neighbors=8, background=0)
        char_candidates = np.zeros(thresh.shape, dtype="uint8")
        for label in np.unique(labels):
            if 0 == label:
                continue
            label_mask = np.zeros(thresh.shape, dtype="uint8")
            label_mask[label == labels] = 255
            contours = cv.findContours(label_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            contours = contours[0] if imutils.is_cv2() else contours[1]
            if 0 < len(contours):
                c = max(contours, cv.contourArea)
                box_x, box_y, box_w, box_h = cv.boundingRect(c)
                aspect_ratio = box_w / float(box_h)
                solidity = cv.contourArea(c) / float(box_w * box_h)
                height_ratio = box_h / float(plate.shape[0])
                keep_as_pect_ratio = aspect_ratio < 1.0
                keep_solidity = solidity > 0.15
                keep_height = 0.4 < height_ratio < 0.95
                if keep_as_pect_ratio and keep_solidity and keep_height:
                    hull = cv.convexHull(c)
                    cv.drawContours(char_candidates, [hull], -1, 255, -1)
        char_candidates = segmentation.clear_border(char_candidates)

        # 有时我们检测到的字符数超过了所需的数量 -
        # 应用一种方法来“修剪”不需要的字符是明智的
        # 返回包含车牌的车牌区域对象，阈值 ＃车牌和人物候选
        return LICENSE_PLATE(success=True, plate=plate, thresh=thresh, candidates=char_candidates)