#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
OpenCV DNN支持YOLO对象检测网络运行

    OpenCV DNN模块支持YOLO对象检测网络，YOLOv3版本同时还发布了移动端支持的网络模型YOLOv3-tiny版本，速度可以在CPU端实时运行的对象检测网
络，OpenCV中通过对DarkNet框架集成支持实现YOLO网络加载与检测。因为YOLOv3对象检测网络是多个层的合并输出，所以在OpenCV中调用时候必须显示声明
那些是输出层，这个对于对象检测网络，OpenCV提供了一个API来获取所有的输出层名称.

API描述如下
    cv.dnn.net.getUnconnectedOutLayersNames()
该函数返回所有非连接的输出层。

调用时候，必须显式通过输入参数完成推断，相关API如下：
    cv.dnn.net.forward(outBlobNames)
        - outBlobNames 是所有输出层的名称,上一个API输出的结果

跟SSD/Faster-RCNN出来的结构不一样，YOLO的输出前四个为
# [center_x, center_y, width, height]
要根据score大小就可以得到score最大的对应对象类别，解析检测结果。

相关模型下载到YOLO的(官方网站)[https://pjreddie.com/darknet/yolo/]

相关推荐文章
    (对象检测网络中的NMS算法详解)[https://mp.weixin.qq.com/s/yccBloK5pOVxDIFkmoY7xg]
    (OpenCV中使用YOLO对象检测)[https://mp.weixin.qq.com/s/95hftpJfSDIMlMVOC7iq4g]
"""

bin_model = "../../../raspberry-auto/models/yolo/yolov3.weights"
config = "../../../raspberry-auto/models/yolo/yolov3.cfg"
label = "../../../raspberry-auto/models/yolo/object_detection_classes_yolov3.txt"


def main():
    image = cv.imread("../../../raspberry-auto/pic/objects.jpg")
    labels = None
    with open(label, "r") as f:
        labels = f.read().rstrip("\n").split("\n")
    print(labels)
    dnn = cv.dnn.readNetFromDarknet(config, bin_model)

    # 获得所有层名称与索引
    layer_names = dnn.getLayerNames()
    last_layer_id = dnn.getLayerId(layer_names[-1])
    last_layer = dnn.getLayer(last_layer_id)
    print(last_layer.type)

    h, w = image.shape[:2]
    data = cv.dnn.blobFromImage(image, 1.0 / 255.0, (416, 416), None, False, False)
    out_names = dnn.getUnconnectedOutLayersNames()
    dnn.setInput(data)
    outs = dnn.forward(out_names)
    t, _ = dnn.getPerfProfile()
    txt = "Inference time: %.2f ms" % (t * 1000.0 / cv.getTickFrequency())
    cv.putText(image, txt, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    # print(outs)
    print(" --------------------- >")
    print(txt)

    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if 0.5 < confidence:
                center_x = int(detection[0] * w)
                center_y = int(detection[1] * h)
                width = int(detection[2] * w)
                height = int(detection[3] * h)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                class_ids.append(int(class_id))
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    indices = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    for i in indices:
        i = i[0]
        box = boxes[i]
        left, top, width, height = box[:4]
        cv.rectangle(image, (left, top), (left + width, top + height), (0, 0, 255), 2, cv.LINE_AA)
        cv.putText(image, labels[class_ids[i]], (left, top), cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 2)

    cv.imshow("dst", image)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
