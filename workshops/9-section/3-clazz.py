#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
    角点检测 - 亚像素级别角点检测
        角点检测用于物体特征提取与特征匹配，但由于角点检测的结果不够精准，因为真实的计算中有些位置可能实在浮点数空间才是最大值，而通过像
    素领域空间进行拟合，实现亚像素级别的焦点检测。相关opencv的api如下：
    
    cv.cornerSubPix(gray, corners, win_size, zero_zone, criteria)
        - gray： 单通道图像，dtype可以为int32、int0、float32等
        - corners： 角点
        - win_size： 差值计算时窗口大小
        - zero_zone： 窗口中间的边长的一半，可以用于避免相关矩阵的奇异性，如果设置为(-1, -1)则表示没有这个区域
        - criteria： 角点精准化迭代过程的终止条件
"""


def process(frame):
    # 1 - shi-tomas角点检测
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    corners = cv.goodFeaturesToTrack(gray, 100, 0.05, 10)
    print("corners is %d" % len(corners))
    for pt in corners:
        b = np.random.randint(0, 256)
        g = np.random.randint(0, 256)
        r = np.random.randint(0, 256)
        cv.circle(frame, (np.int32(pt[0][0]), np.int32(pt[0][1])), 5, (b, g, r), 2)
    # 2 - 亚像素级别角点补充
    win_size = (5, 5)
    zero_zone = (-1, -1)
    criteria = (cv.TERM_CRITERIA_EPS + cv.TermCriteria_COUNT, 40, 0.001)
    corners = cv.cornerSubPix(gray, corners, win_size, zero_zone, criteria)
    for i in range(corners.shape[0]):
        print(" -- Refined Corner [%d] (%d, %d)" % (i, corners[i, 0, 0], corners[i, 0, 1]))
    return frame


def main():
    capture = cv.VideoCapture(0)
    while True:
        ret, frame = capture.read()
        if True is not ret:
            print("can't read any video")
            break
        frame = process(frame)
        cv.imshow("frame", frame)
        key = cv.waitKey(10)
        if 27 == key:  # ESC
            break
    capture.release()
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
