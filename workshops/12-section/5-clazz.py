#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
OpenCV DNN基于残差网络的人脸检测
    OpenCV在DNN模块中提供了基于残差SSD网络训练的人脸检测模型，该模型分别提供了tensorflow版本，caffe版本，torch版本模型文件，
其中tensorflow版本的模型做了更加进一步的压缩优化，大小只有2MB左右，非常适合移植到移动端使用.
    与HAAR与LBP级联检测器对比, DNN 在25毫秒均可以检测出结果，网络支持输入size大小为300x300.
"""

model = "../../../raspberry-auto/models/face_detector/opencv_face_detector_uint8.pb"
config_text = "../../../raspberry-auto/models/face_detector/opencv_face_detector.pbtxt"


def main():
    image = cv.imread("../../../raspberry-auto/pic/70eb501cjw1dwp7pecgewj.jpg")
    net = cv.dnn.readNetFromTensorflow(model, config_text)
    h, w, _ = image.shape
    data = cv.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0), False, False)
    net.setInput(data)
    out = net.forward()
    t, _ = net.getPerfProfile()
    label = "Inference time: %.2f ms" % (t * 1000.0 / cv.getTickFrequency())
    cv.putText(image, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
    for det in out[0, 0, :, :]:
        score = float(det[2])
        if 0.5 < score:
            left = det[3] * w
            top = det[4] * h
            right = det[5] * w
            bottom = det[6] * h
            cv.rectangle(image, (int(left), int(top)), (int(right), int(bottom)), (255, 0, 0), 2)
            cv.putText(image, "score: %.2f" % score, (int(left), int(top)),
                       cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    cv.imshow("face-detection-demo", image)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
