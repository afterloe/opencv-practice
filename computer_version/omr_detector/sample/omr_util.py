#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import imutils
from imutils.contours import sort_contours
from imutils.perspective import four_point_transform
import numpy as np
import os


class OMRUtil(object):
    __step = 300

    def __init__(self, path_of_image="resources/demo.png"):
        if not os.path.isfile(path_of_image):
            print("can't find any image")
            exit(0)
        self.__image = cv.imread(path_of_image)
        self.__answer_key = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}  # omr 答案 第一题B, 第二题E, 第三题A, 第四题D, 第五题B

    def detector(self):
        """
        未考虑OMR 未涂写或 重复涂写的情况

        :return:
        """
        h, w = self.__image.shape[: 2]
        ratio = h / float(self.__step)
        image = imutils.resize(self.__image, height=self.__step)
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        blurred = cv.bilateralFilter(gray, 5, 20, 20)
        edged = cv.Canny(blurred, 70, 200)
        contours = cv.findContours(edged, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv.contourArea, reverse=True)[: 3]
        paper_contour = None
        for contour in contours:
            peri = cv.arcLength(contour, True)
            approx = cv.approxPolyDP(contour, 0.05 * peri, True)
            if 4 == len(approx):
                paper_contour = approx
                break
        warped = four_point_transform(self.__image, paper_contour.reshape(4, 2) * ratio)
        return warped

    def infer(self, paper):
        if None is paper:
            print("please input paper page")
            return
        warped_gray = cv.cvtColor(paper, cv.COLOR_BGR2GRAY)
        # thresh = cv.threshold(warped_gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
        thresh = cv.adaptiveThreshold(warped_gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 45, 15)
        contours = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        queue = []
        for contour in contours:
            x, y, w, h = cv.boundingRect(contour)
            # roi 区域是一个 圆形, 所以计算宽高比
            ar = w / float(h)
            # 圆形的宽高比应该在 1左右， 阈值可动态调整
            if w >= 20 and h >= 20 and 0.9 <= ar <= 1.1:
                queue.append(contour)
        # imutils.contours 的轮廓排序算法 method 有 right-to-left， left-to-right， bottom-to-top， top-to-bottom
        queue = sort_contours(queue, method="top-to-bottom")[0]
        correct = 0
        # 对每一列进行处理
        for (q, i) in enumerate(np.arange(0, len(queue), 5)):
            # 从左到右进行排序， 默认的
            contours = sort_contours(queue[i: i + 5])[0]
            bubbled = None
            # 循环每一列, 寻找涂黑的地方
            for (j, contour) in enumerate(contours):
                mask = np.zeros(thresh.shape, dtype="uint8")
                cv.drawContours(mask, [contour], -1, 255, -1)
                mask = cv.bitwise_and(thresh, thresh, mask=mask)
                # 计算遮罩内的非零像素
                total = cv.countNonZero(mask)
                # 如果遮罩内的像素大于其他遮罩，默认为选择的答案
                if bubbled is None or total > bubbled[0]:
                    bubbled = (total, j)
            color = (0, 0, 255)
            k = self.__answer_key[q]
            if k == bubbled[1]:
                color = (0, 255, 0)
                correct += 1
            cv.drawContours(paper, [contours[k]], -1, color, 3)
        score = (correct / 5.0) * 100
        print("[score]: {:.2f}%".format(score))
        cv.putText(paper, "%.2f%%" % score, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
        cv.imshow("paper", paper)
        cv.waitKey(0)

    def __del__(self):
        cv.destroyAllWindows()
