#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    视频前景/背景提取
        视频前景/背景提取技术用于提取前景移动对象，通过获取移动对象的mask实现获取移动物体的轮廓信息，最常用的方法是帧差相减法进行，即用
    前一帧的图像最为背景图像与当前帧进行相减，该方法对光照、噪声相当敏感。opencv中对背景模型提取的算法有两种，一种是基于高斯模糊模型（GMM）
    实现背景提取，另外一种是使用最近相邻模型（KNN）实现的，api如下：
    
    GMM cv.createBackgroundSubtractorMOG2(history, varThreshold, detectShadows)
        - history: 过往帧数，默认500帧，历史进行比较
        - varThreshold: 马氏距离，默认16，值越大，最新的像素会归为前景，值越小对光照敏感
        - detectShadow: 是否保留阴影检测，默认True， 开启阴影检测虽然可以提高提取效果，但是效率会变低，推荐不开启
        
    KNN cv.createBackgroundSubtractorKNN()的参数描述如上
        
"""


def main():
    capture = cv.VideoCapture(0)
    # mog2bs = cv.createBackgroundSubtractorKNN(500, 1000, False)  # KNN模型
    mog2bs = cv.createBackgroundSubtractorMOG2(300)  # GMM模型
    while True:
        ret, frame = capture.read()
        if True is not ret:
            print("can't read any video!")
            break
        mask = mog2bs.apply(frame)
        background = mog2bs.getBackgroundImage()
        cv.imshow("input", frame)
        cv.imshow("mask", mask)
        cv.imshow("background", background)
        key = cv.waitKey(10) & 0xff
        if 27 == key:  # ESC
            break
    cv.destroyAllWindows()
    capture.release()


if "__main__" == __name__:
    main()
