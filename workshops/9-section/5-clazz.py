#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
from goto import with_goto
import math
import numpy as np

"""
    KLT光流跟踪法二：
        静止点删除与跟踪轨迹绘制。处置流程为 输入第一帧图像 -> 特征点检测 -> 保持特征点 -> 输入第二帧图像（开始跟踪） -> 跟踪特征点 -> 删除
    损失特征点 -> 保存跟踪特征点 -> 用第二帧图像替换第一帧图像 -> 用后续输入帧替换第二帧 -> 选择新的特征点替换损失的特征点 -> 保存特征点数据
    并回到输入第二帧图像，开始循环。
"""

MAX_CORNERS = 100

features_params = dict(maxCorners=MAX_CORNERS, qualityLevel=0.01, minDistance=10, blockSize=3, mask=None)
lk_params = dict(nextPts=None, winSize=(31, 31), maxLevel=3,
                 criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 30, 0.01))
color_set = np.random.randint(0, 255, (MAX_CORNERS, 3))
# points = []


@with_goto
def main():
    capture = cv.VideoCapture("../../../raspberry-auto/pic/vtest.avi")
    ret, frame = capture.read()
    if True is not ret:
        print("can't read any video")
        goto .end
    prv_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    prv_frame = cv.medianBlur(prv_frame, 3)
    prv_corners = cv.goodFeaturesToTrack(prv_frame, **features_params)
    # points += prv_corners
    while True:
        ret, frame = capture.read()
        if True is not ret:
            print("can't read next frame.")
            break
        next_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        next_frame = cv.medianBlur(next_frame, 3)
        next_corners, status, err = cv.calcOpticalFlowPyrLK(prv_frame, next_frame, prv_corners, **lk_params)
        old_pts = prv_corners[1 == status]
        new_pts = next_corners[1 == status]
        for i, (older, newer) in enumerate(zip(old_pts, new_pts)):
            a, b = older.ravel()
            c, d = newer.ravel()
            width = math.pow(abs(a - c), 2)
            height = math.pow(abs(b - d), 2)
            hypotenuse = math.sqrt(width + height)
            if 2 < hypotenuse:
                cv.circle(frame, (c, d), 5, color_set[i].tolist(), -1)
                cv.line(frame, (c, d), (a, b), color_set[i].tolist(), 2, cv.LINE_8)
        #     else:
        #         new_pts.remove(older)
        # if 40 > len(new_pts):
        #     next_corners, status, err = cv.calcOpticalFlowPyrLK(prv_frame, next_frame, prv_corners, **lk_params)
        #     new_pts = next_corners[1 == status]
        cv.imshow("frame", frame)
        key = cv.waitKey(30) & 0xff
        if 27 == key:
            break
        # 更新前一帧的内容
        prv_frame = next_frame.copy()
        prv_corners = new_pts.reshape(-1, 1, 2)

    label .end
    capture.release()
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
