#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import math
import time

"""

"""

FACE_PROTO = "../../../raspberry-auto/models/face_detector/opencv_face_detector.pbtxt"
FACE_MODEL = "../../../raspberry-auto/models/face_detector/opencv_face_detector_uint8.pb"

AGE_PROTO = "../../../raspberry-auto/models/cnn_age_gender_models/age_deploy.prototxt"
AGE_MODEL = "../../../raspberry-auto/models/cnn_age_gender_models/age_net.caffemodel"

GENDER_PROTO = "../../../raspberry-auto/models/cnn_age_gender_models/gender_deploy.prototxt"
GENDER_MODEL = "../../../raspberry-auto/models/cnn_age_gender_models/gender_net.caffemodel"

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
AGE_LIST = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
GENDER_LIST = ['Male', 'Female']
PADDING = 40


def find_face(image, net, conf_threshold=0.7):
    h, w = image.shape[:2]
    data = cv.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0), False, False)
    net.setInput(data)
    detections = net.forward()
    boxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if conf_threshold < confidence:
            left = int(detections[0, 0, i, 3] * w)
            top = int(detections[0, 0, i, 4] * h)
            right = int(detections[0, 0, i, 5] * w)
            bottom = int(detections[0, 0, i, 6] * h)
            boxes.append([left, top, right, bottom])
            cv.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 2, cv.LINE_8)
    return image, boxes


def main():
    age_net = cv.dnn.readNet(AGE_MODEL, AGE_PROTO)
    gender_net = cv.dnn.readNet(GENDER_MODEL, GENDER_PROTO)
    face_net = cv.dnn.readNet(FACE_MODEL, FACE_PROTO)
    t = time.time()
    image = cv.imread("../../../raspberry-auto/pic/70eb501cjw1dwp7pecgewj.jpg")
    image, boxes = find_face(image, face_net)
    if not boxes:
        print("can't find any face here!")
        return
    h, w = image.shape[:2]
    for box in boxes:
        roi = image[
              max(0, box[1] - PADDING): min(box[3] + PADDING, h - 1),
              max(0, box[0] - PADDING): min(box[2] + PADDING, w - 1)]
        data = cv.dnn.blobFromImage(roi, 1.0, (227, 227), MODEL_MEAN_VALUES, False, False)
        gender_net.setInput(data)
        age_net.setInput(data)
        gender_out = gender_net.forward()
        gender_info = GENDER_LIST[gender_out[0].argmax()]
        cv.putText(image, "%s, %.3f" % (gender_info, gender_out[0].max()), (box[0] - PADDING, box[1] - PADDING),
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
        age_out = age_net.forward()
        age_info = AGE_LIST[age_out[0].argmax()]
        cv.putText(image, "{}, {:.3f}".format(age_info, age_out[0].max()), (box[0], box[3] + PADDING),
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
    print("use time %.3f ms" % (time.time() - t))
    # cv.namedWindow("dst", cv.WINDOW_FREERATIO)
    cv.imshow("dst", image)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
