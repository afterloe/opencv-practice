#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
from goto import with_goto

"""
    基于均值迁移的对象移动分析
        均值迁移移动对象分析主要是基于ROI区域颜色直方图分布与反向投影实现的，其核心思想是对反向投影后的图像作均值迁移（meanshift）
    从而发现密度最高的区域，算法流程如下：
        1 读取图像一帧
        2 绘制HSV直方图
        3 反向投影该帧
        4 使用meanshift算法寻找最大分布密度
    
    cv.meanShift(probImage, window, criteria)
        - probImage: 直方图反向投影的结果
        - window： 搜索窗口， ROI对象区域
        - criteria： 均值迁移停止条件
"""

video_param = "../../../raspberry-auto/pic/vtest.avi"


@with_goto
def main():
    capture = cv.VideoCapture(video_param)
    # 读取第一帧
    ret, frame = capture.read()
    if True is not ret:
        print("can't read any video")
        goto .end
    cv.namedWindow("live", cv.WINDOW_AUTOSIZE)
    x, y, w, h = cv.selectROI("live", frame, True, False)  # 通用api，通过鼠标选取第一帧中的roi区域
    track_window = (x, y, w, h)

    # 获取ROI直方图
    roi = frame[y: y + h, x: x + w]
    hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
    lower = (26, 43, 46)
    upper = (34, 255, 25)
    mask = cv.inRange(hsv_roi, lower, upper)
    roi_hist = cv.calcHist([hsv_roi], [0], mask, [180], [0, 180])
    cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)

    # 设置搜索跟踪分析条件
    term_criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)
    while True:
        ret, frame = capture.read()
        if True is not ret:
            print("video is end")
            break
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        dst = cv.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)  # 直方图反向投影 详见2-day/10-clazz.py
        ret, track_window = cv.meanShift(dst, track_window, term_criteria)
        x, y, w, h = track_window
        cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv.imshow("live", frame)
        key = cv.waitKey(10) & 0xff
        if 27 == key:
            break

    label .end
    capture.release()
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
