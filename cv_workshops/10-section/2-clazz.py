#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    LBP特征检测器
        LBP特征检测器是基于二值图像的的纹理分析，相对与HAAR级联检测器，LBP在小数据量的情况下准确度较高，当训练足够多的时候，LBP与HAAR
    的差距会越来越小。LBP特征检测器将灰度图像转换为二值图像，同时对八领域内的像素按2的阶乘进行排序，将其按位相乘最后求和。该数值可以进行
    表示点、平坦/点区域、线、边缘、角点等内容。LBP的由于大多数计算均为int32或int64计算，相对于HAAR，少了很多浮点数运算，所以在结果计算
    时速度比HAAR快，而且训练出的xml相对于HAAR的小很多。
        使用LBP特征检测器与HAAR的方式相同，只是参数不一样
"""

LBP_param = "/Users/afterloe/Project/lib/opencv/data/lbpcascades/lbpcascade_frontalface.xml"
video_param = 0
multi_param = dict(scaleFactor=1.05, minNeighbors=1, minSize=(120, 120), maxSize=(520, 520))


def main():
    capture = cv.VideoCapture(video_param)
    detector = cv.CascadeClassifier(LBP_param)
    while True:
        ret, frame = capture.read()
        if True is not ret:
            print("video is end.")
            break
        faces = detector.detectMultiScale(frame, **multi_param)
        for x, y, w, h in faces:
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, cv.LINE_AA)
        cv.imshow("main", frame)
        key = cv.waitKey(60) & 0xff
        if 27 == key:  # esc
            break
    cv.destroyAllWindows()
    capture.release()


if "__main__" == __name__:
    main()
