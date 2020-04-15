#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
OpenCV DNN 支持YOLOv3-tiny版本实时对象检测
    相比YOLOv3，YOLOv3-tiny只有两个输出层，而且权重参数层与参数文件大小都大大的下降，可以在嵌入式设备与前端实时运行, 大小只有30MB左右
"""

bin_model = "../../../raspberry-auto/models/yolo/yolov3-tiny.weights"
config_path = "../../../raspberry-auto/models/yolo/yolov3-tiny.cfg"
label_path = "../../../raspberry-auto/models/yolo/object_detection_classes_yolov3.txt"


def main():
    capture = cv.VideoCapture("../../../raspberry-auto/pic/G19.mp4")
    classes = None
    with open(label_path, "r") as f:
        classes = f.read().rstrip("\n").split("\n")
    net = cv.dnn.readNetFromDarknet(config_path, bin_model)
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)
    layer_name = net.getUnconnectedOutLayersNames()
    while True:
        ret, frame = capture.read()
        if False is ret:
            print("video is end.")
            break
        h, w = frame.shape[:2]
        data = cv.dnn.blobFromImage(frame, 0.055, (416, 416), None, False, False)
        net.setInput(data)
        outs = net.forward(layer_name)
        t, _ = net.getPerfProfile()
        fps = 1000 / (t * 1000.0 / cv.getTickFrequency())
        txt = "FPS: %.2f" % fps
        cv.putText(frame, txt, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
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
            cv.rectangle(frame, (left, top), (left + width, top + height), (255, 0, 0), 2, cv.LINE_AA)
            cv.putText(frame, classes[class_ids[i]], (left, top), cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 2)
        key = cv.waitKey(1)
        if 27 == key:
            print("enter esc.")
            break
        cv.imshow("yolov3-tiny dst", frame)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
