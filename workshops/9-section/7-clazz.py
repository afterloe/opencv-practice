#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
from goto import with_goto
import imutils
import numpy as np

"""
    视频分析 - 基于帧差法实现移动对象分析
        光流跟踪与背景消除都是基于建模(KNN、高斯)的方式进行的，其实，有一种原始的方式较移动分析更为有效，这就是基于帧差法实现
    移动对象分析，在监控或固定视角效果明显，帧差法进一步划分可以分为两帧差与三帧差，具体描述如下：
        两帧差： diff = frame - prev，即当前帧减前一帧
        三帧差： diff_1 = prev_2 - prev_1; diff_2 = frame - prev_1
                diff = diff_1 & diff_2
        帧差法在求取帧差之前进行高斯模糊，可用于降低干扰，通过得到的diff图像进行形态学操作，用于合并与候选区域，提升效率。但帧差
    法的缺点如下：一是高斯模糊是高耗时的计算，越模糊效果越好，但耗时越长；二是该方法容易受到噪声与光线干扰。
"""
video_param = "../../../raspberry-auto/pic/vtest.avi"
gaussian_param = dict(ksize=(0, 0), sigmaX=13)
threshold_param = dict(thresh=0, maxval=255, type=cv.THRESH_BINARY | cv.THRESH_OTSU)
kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
morphology_param = dict(op=cv.MORPH_OPEN, kernel=kernel)


def process(frame):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, **gaussian_param)
    return blur


@with_goto
def main():
    # 三帧差
    capture = cv.VideoCapture(0)
    ret, prev_1 = capture.read()
    if True is not ret:
        print("can't read any frame")
        goto .end
    ret, prev_2 = capture.read()
    if True is not ret:
        print("video is end.")
        goto .end
    prev_1 = process(prev_1)
    prev_2 = process(prev_2)
    while True:
        ret, frame_src = capture.read()
        if True is not ret:
            print("video is end.")
            break
        frame = process(frame_src)
        diff_1 = cv.subtract(prev_2, prev_1)
        diff_2 = cv.subtract(frame, prev_1)
        diff = cv.bitwise_and(diff_1, diff_2)
        _, binary = cv.threshold(diff, **threshold_param)
        binary = cv.morphologyEx(binary, **morphology_param)
        prev_1 = np.copy(prev_2)
        prev_2 = np.copy(frame)
        cv.imshow("video", frame_src)
        cv.imshow("result", binary)
        key = cv.waitKey(10) & 0xff
        if 27 == key:  # esc
            break

    label .end
    capture.release()
    cv.destroyAllWindows()


def main_1():
    capture = cv.VideoCapture(video_param)
    # 两帧法演示
    ret, prev_frame = capture.read()
    if True is not ret:
        print("can't read any frame")
        goto .end
    prev_gray = cv.cvtColor(prev_frame, cv.COLOR_BGR2GRAY)
    gaussian_param["src"] = prev_gray
    prev_blur = cv.GaussianBlur(**gaussian_param)
    while True:
        ret, frame = capture.read()
        if True is not ret:
            print("video is end.")
            break
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gaussian_param["src"] = gray
        blur = cv.GaussianBlur(**gaussian_param)
        diff = cv.subtract(blur, prev_blur)
        threshold_param["src"] = diff
        _, binary = cv.threshold(**threshold_param)
        morphology_param["src"] = binary
        binary = cv.morphologyEx(**morphology_param)
        contours = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        for cnt in contours:
            x, y, w, h = cv.boundingRect(cnt)
            cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2, cv.LINE_AA)
        cv.imshow("video", frame)
        cv.imshow("result", binary)
        prev_blur = np.copy(blur)
        key = cv.waitKey(10) & 0xff
        if 27 == key:  # esc
            break

    label .end
    capture.release()
    cv.destroyAllWindows()


if "__main__" == __name__:
    # main_1()
    main()
