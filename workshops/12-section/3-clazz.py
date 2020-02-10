#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
OpenCV DNN基于SSD实现对象检测
    openCV 4.0后支持常见得对象检测模型SSD， 以及它的移动版Mobile Net-SSD，特别是后者在端侧边缘设备上可以实时计算，基于Caffe训练好的
mobile-net SSD支持20类别对象检测（可参考classes_path描述文件）。

推断API如下
    cv.dnn.net.forward(outputName)
        - outputName 参数缺省为空，或Array

该API会返回一个四维的tensor，前两个维度是1，后面的两个维度，分别表示检测到BOX数量，以及每个BOX的坐标，对象类别，得分等信息。需要注意的是，这
个坐标是浮点数的比率，不是像素值，所以必须转换为像素坐标才可以绘制BOX/矩形

OpenCV DNN加速文章 (->)[https://mp.weixin.qq.com/s/bM3jKtV9BbMFm5p6O2S3yg]
"""

bin_model = "../../../raspberry-auto/models/ssd/MobileNetSSD_deploy.caffemodel"
prototxt = "../../../raspberry-auto/models/ssd/MobileNetSSD_deploy.prototxt"
classes_path = "../../../raspberry-auto/models/ssd/labelmap_det.txt"

objName = ["background",
"aeroplane", "bicycle", "bird", "boat",
"bottle", "bus", "car", "cat", "chair",
"cow", "diningtable", "dog", "horse",
"motorbike", "person", "pottedplant",
"sheep", "sofa", "train", "tvmonitor"]


def main():
    image = cv.imread("../../../raspberry-auto/pic/dog.jpg")
    classes = None
    with open(classes_path, "r") as f:
        classes = f.read().rstrip("\n").split("\n")
    print(classes)
    cv.imshow("src", image)
    blob_image = cv.dnn.blobFromImage(image, 0.007843, (300, 300), (127.5, 127.5, 127.5), True, crop=False)
    net = cv.dnn.readNetFromCaffe(prototxt, bin_model)
    net.setInput(blob_image)
    cv_out = net.forward()
    # print(cv_out)
    h, w, ch = image.shape
    for detection in cv_out[0, 0, :, :]:
        score = float(detection[2])
        obj_index = int(detection[1])
        word = "score:%.2f, %s" % (score, objName[obj_index] if classes else "not_found")
        if 0.5 < score:
            left = detection[3] * w
            top = detection[4] * h
            right = detection[5] * w
            bottom = detection[6] * h
            cv.rectangle(image, (int(left), int(top), int(right), int(bottom)), (255, 0, 0), 2)
            cv.putText(image, word, (int(left) - 10, int(top) - 5), cv.FONT_HERSHEY_SIMPLEX, 0.7,
                       (0, 255, 0), 2, cv.LINE_8)
            print(word)
    cv.imshow("result", image)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
