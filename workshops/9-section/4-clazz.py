#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
from goto import with_goto  # 引入goto的包，少些一些无关的代码
import numpy as np

"""
    KLT光流跟踪算法
        光流跟踪算法分为稠密光流跟踪与稀疏光流跟踪两种，而KLT属于稀疏光流跟踪算法，该算法工作需要3个假设的前提条件**一是亮度恒定，即光照条件
    不会频繁变动；而是短距离移动，即物体移动幅度不大，不会出现超长距离的快速移动；三是空间一致性，由于KLT算法默认左上角为坐标轴(0, 0)的起点，
    摄像头角度不会进行变动，否则结果会出现大面积的偏差**，有关KLT光流跟踪算法的api描述如下：
    
    cv.calcOpticalFlowPyrLK(prevImg, nextImg, prevPts, nextPts [, status=None, err=None, winSize=None, maxLevel=None,
                            criteria=None, flags=None, minEigThreshold=None])
        - prevImg: 前一张单通道灰度图像，dtype可以为int32、int0或float32等
        - nextImg: 当前的单通道灰度图像，dtype可以为int32、int0或float32等 
        - prevPts: 前一张图像中的角点
        - nextPts: 当前图像中的光流点；若为None，则作为输出参数
        
        可选参数
        - status: 输出状态，1表示正常改点保留，否则舍弃；若为None，则作为输出参数
        - err: 错误信息；若为None，则作为输出参数
        - winSize: 光流算法对象的开窗大小
        - maxLevel: 金字塔层数，0表示只检测当前图像，不构建金字塔
        - criteria: 光流算法停止条件
        
    eg: nextPts, status, err = cv.calcOpticalFlowPyrLK(**param)
"""


"""
    dict: python3的基本数据类型，类似于map， 采用key-value存储，支持for循环，使用 **开头可用于方法解构
"""
# 角点检测参数
feature_params = dict(maxCorners=100, qualityLevel=0.01, minDistance=10, blockSize=3)
# KLT光流参数
lk_params = dict(winSize=(31, 31), maxLevel=3, criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 30, 0.01))
# 随机颜色
# numpy.random.randint(low, high=None, size=None, dtype='l')
# size: int or tuple of ints(可选)
# 输出随机数的尺寸，比如size = (m * n* k)则输出同规模即m * n* k个随机数。默认是None的，仅仅返回满足要求的单一随机数。
color = np.random.randint(0, 255, (100, 3))  # 每次生成 100行，取100的原因是角点检测最多输出100个点，每行具有3个值 描述如下：
"""
    output -> array([0, 0, 2], [10, 20, 33] ...)
"""


@with_goto
def main():
    capture = cv.VideoCapture(0)
    # KLT 算法参数初始化
    ret, pre_frame = capture.read()
    if True is not ret:
        print("can't read video")
        goto .end
    # 灰度转换
    pre_frame = cv.cvtColor(pre_frame, cv.COLOR_BGR2GRAY)
    # 计算角点
    pre_corners = cv.goodFeaturesToTrack(pre_frame, mask=None, **feature_params)
    while True:
        ret, frame = capture.read()
        if True is not ret:
            print("video is stop!")
            break
        now_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        now_corners, st, err = cv.calcOpticalFlowPyrLK(pre_frame, now_frame, pre_corners, None, **lk_params)
        good_new = now_corners[st == 1]
        good_old = pre_corners[st == 1]
        # 绘制跟踪线
        # enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中
        # zip() 函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的对象，这样做的好处是节约了不少的内存。
        # 一般用于两个以上的参数循环
        for i, (newer, older) in enumerate(zip(good_new, good_old)):
            # ravel 将多维数组 转换为 一维数组
            a, b = newer.ravel()
            c, d = older.ravel()
            frame = cv.line(frame, (a, b), (c, d), color[i].tolist(), 2)
            frame = cv.circle(frame, (a, b), 5, color[i].tolist(), -1)
        cv.imshow("frame", frame)
        key = cv.waitKey(30) & 0xff
        if 27 == key:
            break
        # 更新
        pre_frame = now_frame.copy()
        pre_corners = good_new.reshape(-1, 1, 2)

    label .end
    capture.release()
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
