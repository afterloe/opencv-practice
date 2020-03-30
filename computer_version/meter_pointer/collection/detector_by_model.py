#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import time
import numpy as np

"""

"""

bin_model = "../../../../raspberry-auto/models/yolo/yolov3-tiny.weights"
config = "../../../../raspberry-auto/models/yolo/yolov3-tiny.cfg"
label = "../../../../raspberry-auto/models/yolo/object_detection_classes_yolov3.txt"


def main():
    capture = cv.VideoCapture(0)
    dnn = cv.dnn.readNetFromDarknet(config, bin_model)
    dnn.setPreferableBackend(cv.dnn.DNN_BACKEND_DEFAULT)
    dnn.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)
    cv.namedWindow("yolov3 demo")
    cv.resizeWindow("yolov3 demo", 600, 300)

    while True:
        ret, frame = capture.read()
        if False is ret:
            print("video is ended.")
            break
        h, w = frame.shape[:2]
        data = cv.dnn.blobFromImage(frame, 1.0 / 255.0, (416, 416), None, False, False)
        out_names = dnn.getUnconnectedOutLayersNames()
        dnn.setInput(data)
        outs = dnn.forward(out_names)
        # t, _ = dnn.getPerfProfile()
        # txt = "Inference time: %.2f ms" % (t * 1000.0 / cv.getTickFrequency())
        # cv.putText(frame, txt, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                if class_id != 74:
                    continue
                confidence = scores[class_id]
                if 0.5 < confidence:
                    center_x = int(detection[0] * w)
                    center_y = int(detection[1] * h)
                    width = int(detection[2] * w)
                    height = int(detection[3] * h)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])
        indices = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        for i in indices:
            i = i[0]
            box = boxes[i]
            left, top, width, height = box[:4]
            cv.rectangle(frame, (left, top), (left + width, top + height), (0, 0, 255), 2, cv.LINE_AA)
            cv.putText(frame, "target", (left, top), cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 2)

        cv.imshow("yolov3 demo", frame)
        key = cv.waitKey(100)
        if 27 == key:
            print("enter esc")
            break
        if 119 == key:
            print("enter w to save image.")
            cv.imwrite("%s.jpeg" % (time.strftime("%Y-%d-%H-%M-%S", time.gmtime(time.time()))), frame,
                       [cv.IMWRITE_JPEG_QUALITY, 100])
    capture.release()


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
