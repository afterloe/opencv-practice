#!/usr/bin/env python3
# -*- coding=utf-8 -*-


import cv2 as cv
from goto import with_goto
import numpy as np


"""
    稠密光流分析
        光流分析分稀疏与稠密两种，在opencv 4.0后Opencv支持两种稠密光流计算方法
    相关api如下:

    cv.calcOpticalFlowFarneback(prev, next, flow, pyr_scale, levels, winsize, iterations, poly_n, poly_sigma, flags)
        - prev: 前一帧的灰度图像
        - next: 当前帧的灰度图像
        - flow: 输出的光流
        - pyr_scale: 金字塔缩放比率
        - levels: 金字塔层数
        - winszie: 开窗计算的窗口大小
        - iterations: 迭代计算的次数
        - poly_n: 生成光流时，对领域像素的多项展开，n越大越模糊，越稳定
        - poly_sigma: 高斯系数，和n成正相关，当n增大时，sigma对应增大
        - flags: OPTFLOW_USE_INITIAL_FLOW 盒子模糊进行光流初始化
                 OPTFLOW_FARNEBACK_GAUSSIAN 高斯模糊

"""


flow_params = dict(flow=None, pyr_scale=0.5, levels=3, winsize=15, iterations=3, poly_n=5, poly_sigma=1.2,
                   flags=cv.OPTFLOW_FARNEBACK_GAUSSIAN)  # 高斯


@with_goto
def main():
    capture = cv.VideoCapture(0)
    ret, frame = capture.read()
    if True is not ret:
        print("can't read video!")
        goto .end
    prv_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame)  # 图像的另外一种复制算法， 初始化为0， dtype与shape同原图相同
    hsv[..., 1] = 255  # 一种新的写法，将hsv色系中的s通道 转换为 255
    while True:
        ret, frame = capture.read()
        if True is not ret:
            print("video is end!")
            break
        next_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        flow_params["prev"] = prv_frame
        flow_params["next"] = next_frame
        flow = cv.calcOpticalFlowFarneback(**flow_params)
        # flow = cv.calcOpticalFlowFarneback(prv_frame, next_frame, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        # 空间坐标系转换
        mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])
        hsv[..., 0] = ang * 180 / np.pi / 2  # 固定公式， 将角度转换为对应的h通道的值
        hsv[..., 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)  # 对v通道的值进行归一化操作
        bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
        cv.imshow("frame", bgr)
        key = cv.waitKey(1) & 0xff
        if 27 == key:
            break
        # 重置
        prv_frame = next_frame

    label .end
    capture.release()
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()

