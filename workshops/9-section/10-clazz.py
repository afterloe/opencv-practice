#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
from goto import with_goto
import numpy as np

"""
    移动对象的轨迹绘制
        通过对移动对象进行连续自适应均值分析后，对返回的内容获取中心坐标点，并将中心坐标点放入点阵集合，通过点阵集合绘制其运动路径。大致
    步骤如下：
        1 初始化路径点集
        2 对每帧的轮廓进行中心化坐标提取
        3 添加坐标到点集的最后位置
        4 绘制路径曲线
"""

video_param = "../../../raspberry-auto/pic/balltest.mp4"


@with_goto
def main():
    capture = cv.VideoCapture(video_param)
    ret, frame = capture.read()
    if True is not ret:
        print("video can't read!")
        goto .end
    # ROI 区域提取
    cv.namedWindow("main", cv.WINDOW_AUTOSIZE)
    trajectory = []
    x, y, w, h = cv.selectROI("main", frame, True, False)
    track_window = (x, y, w, h)
    roi = frame[y: y + h, x: x + w]
    roi_hsv = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
    mask = cv.inRange(roi_hsv, (26, 43, 46), (34, 255, 255))
    roi_hist = cv.calcHist([roi_hsv], [0], mask, [180], [0, 180])
    roi_hist = cv.normalize(roi_hist, None, 0, 255, cv.NORM_MINMAX)
    term_criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)
    while True:
        ret, frame = capture.read()
        if True is not ret:
            print("video is end")
            break
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        dst = cv.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
        track_box = cv.CamShift(dst, track_window, term_criteria)
        track_window = track_box[1]
        pt = np.int32(track_box[0][0])
        if 0 < pt[0] and 0 < pt[1]:
            trajectory.append(pt)
        if 100 < len(trajectory):
            del(trajectory[0])
        cv.ellipse(frame, track_box[0], (0, 0, 255), 3, cv.LINE_8)
        for i in range(1, len(trajectory), 1):
            cv.line(frame, (trajectory[i - 1][0], trajectory[i - 1][1]),
                    (trajectory[i][0], trajectory[i][1]), (255, 0, 0), 2, cv.LINE_AA)
        cv.imshow("main", frame)
        key = cv.waitKey(10)
        if 27 == key:  # esc
            break
    label .end
    capture.release()
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
