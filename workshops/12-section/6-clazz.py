#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
OpenCV DNN 基于残差网络的视频人脸检测
    支持单精度的fp16的检测准确度更好的Caffe模型加载与使用，这里实现了一个基于Caffe Model的视频实时人脸监测模型
"""


bin_model = "../../../raspberry-auto/models/face_detector/res10_300x300_ssd_iter_140000_fp16.caffemodel"
config = "../../../raspberry-auto/models/face_detector/deploy.prototxt"


def process(image, net):
    h, w = image.shape[:2]
    data = cv.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 117.0, 123.0), False, False)
    net.setInput(data)
    out = net.forward()
    t, _ = net.getPerfProfile()
    fps = 1000 / (t * 1000.0 / cv.getTickFrequency())
    label = "FPS: %.2f" % fps
    cv.putText(image, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
    for det in out[0, 0, :, :]:
        score = float(det[2])
        if 0.5 < score:
            left = int(det[3] * w)
            top = int(det[4] * h)
            right = int(det[5] * w)
            bottom = int(det[6] * h)
            cv.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 2)
            cv.putText(image, "score: %.2f" % score, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
    return image


def main():
    capture = cv.VideoCapture("../../../raspberry-auto/pic/two_red_line.mp4")
    dnn = cv.dnn.readNetFromCaffe(config, bin_model)
    dnn.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    dnn.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)
    while True:
        ret, frame = capture.read()
        if False is ret:
            print("can't read next frame.")
            break
        result = process(frame, dnn)
        cv.imshow("face-detector-video", result)
        key = cv.waitKey(2)
        if 27 == key:
            print("enter ese!")
            break
    capture.release()


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
