#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
from goto import with_goto

"""
    基于连续自适应均值迁移（CAM）的对象移动分析
        CAM是连续自适应的均值迁移跟踪算法，相对于均值迁移相比较他的主要改进点有两处，一是会根据跟踪对象大小变化自动
    调整搜索窗口大小；二是会返回更为完整的位置信息，其中包括了位置坐标及角度

    cv.CamShift(probImage, window, criteria)
        - probImage: 输入图像，直方图方向投影结果
        - window: 搜索开窗大小，ROI对象区域
        - criteria: 均值迁移停止条件

    注：返回信息中需要手动更新开窗信息
"""

video_param = "../../../raspberry-auto/pic/balltest.mp4"


@with_goto
def main():
    capture = cv.VideoCapture(video_param)
    ret, frame = capture.read()
    if True is not ret:
        print("can't read any video!")
        goto .end
    cv.namedWindow("live", cv.WINDOW_AUTOSIZE)
    x, y, w, h = cv.selectROI("live", frame, True, False)
    track_window = (x, y, w, h)
    roi = frame[y: y + h, x: x + w]
    hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv_roi, (26, 43, 46), (34, 255, 255))
    roi_hist = cv.calcHist([hsv_roi], [0], mask, [180], [0, 180])
    cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)
    term_criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)
    while True:
        ret, frame = capture.read()
        if True is not ret:
            print("video is end.")
            break
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        dst = cv.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
        track_box = cv.CamShift(dst, track_window, term_criteria)
        track_window = track_box[1]
        print(track_box)
        cv.ellipse(frame, track_box[0], (0, 0, 255), 3, cv.LINE_8)
        cv.imshow("live", frame)
        key = cv.waitKey(10)
        if 27 == key:  # esc
            break
    label .end
    capture.release()
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
