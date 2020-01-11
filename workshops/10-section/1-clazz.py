#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
    对象检测 - HAAR级联检测器
        opencv中使用HAAR级联检测器支持人脸检测、微笑、眼镜与嘴巴检测等，通过opencv源码中已训练好的xml模型数据可实现相关对象检测。api
    如下：
    
    cv.CascadeClassifier.detectMultiScale(image, scaleFactor, minNeighbors, flags, minSize, maxSize)
        - image: 输入图像
        - scaleFactor: 放缩比率
        - minNeighbors: 最低相邻矩形框
        - flags: 0，被淘汰
        - minSize：检测的最小人脸
        - maxSize: 检测的最大人脸
"""

video_param = 0
multi_param = dict(scaleFactor=1.05, minNeighbors=1, minSize=(120, 120), maxSize=(520, 520))
cascade_param = cv.data.haarcascades + "haarcascade_frontalface_alt.xml"


def main():
    capture = cv.VideoCapture(video_param)
    detector = cv.CascadeClassifier(cascade_param)
    while True:
        ret, frame = capture.read()
        if True is not ret:
            print("video is end.")
            break
        faces = detector.detectMultiScale(frame, **multi_param)
        for x, y, w, h in faces:
            cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2, cv.LINE_AA)
        cv.imshow("main", frame)
        key = cv.waitKey(50) & 0xff
        if 27 == key:  # esc
            break
    capture.release()
    cv.destroyAllWindows()


if "__main__" == __name__:
    main()
