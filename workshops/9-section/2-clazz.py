#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
    角点检测算法 - shi-tomas角点检测
        harris角点检测算法计算速度慢，很难实时计算，最常用的角点检测算法是shi-tomas，opencv中相关API描述如下：
        
    cv.goodFeaturesToTrack(gray, maxCorners, qualityLevel, minDistance [, mask, blockSize, useHarrisDetector, k])
        - gray: 单通道图像，dtype可以为int32、int32、float32等
        - maxCorners: 最多返回多少个角点
        - qualityLevel: 丢弃阈值， 关键点R < qualityLevel * max_response则会被放弃运算，经验值0.05
        - minDistance: 两个关键点之间的最短距离
        
        可选参数
        - mask: 做角点检测的mask区域，传入表示只在该区域内做角点检测
        - blockSize: 梯度与微积分的开窗区域 
        - useHarrisDetector: 是否使用harris角点检测， bool，默认为false
        - k: 启动harris检测时才有用，表示soble算子系数，默认是 0.04， 经验值 0.04 ~ 0.06
"""


def process(frame):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    corners = cv.goodFeaturesToTrack(gray, 100, 0.05, 10)
    for pt in corners:
        b = np.random.randint(0, 256)
        g = np.random.randint(0, 256)
        r = np.random.randint(0, 256)
        cv.circle(frame, (np.int32(pt[0][0]), np.int32(pt[0][1])), 5, (b, g, r), 2)
    return frame


def main():
    capture = cv.VideoCapture(0)
    while True:
        ret, frame = capture.read()
        if True is not ret:
            print("can't read any video")
            break
        frame = process(frame)
        cv.imshow("liv...", frame)
        key = cv.waitKey(10) & 0xff
        if 27 == key:  # ESC
            break
    cv.destroyAllWindows()
    capture.release()


if "__main__" == __name__:
    main()
