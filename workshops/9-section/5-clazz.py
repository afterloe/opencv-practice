#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
from goto import with_goto

"""
    KLT光流跟踪法二：
        静止点删除与跟踪轨迹绘制。处置流程为 输入第一帧图像 -> 特征点检测 -> 保持特征点 -> 输入第二帧图像（开始跟踪） -> 跟踪特征点 -> 删除
    损失特征点 -> 保存跟踪特征点 -> 用第二帧图像替换第一帧图像 -> 用后续输入帧替换第二帧 -> 选择新的特征点替换损失的特征点 -> 保存特征点数据
    并回到输入第二帧图像，开始循环。
"""


def main():
    capture = cv.VideoCapture(0)
    ret, frame = capture.read()
    if True is not ret:
        print("can't read any video")
        goto .end

    lable .end
    capture.release()
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
