#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""

"""

ssd_bin = "../../../raspberry-auto/models/ssd/MobileNetSSD_deploy.caffemodel"
ssd_config = "../../../raspberry-auto/models/ssd/MobileNetSSD_deploy.prototxt"
# classes_path = "../../../raspberry-auto/models/ssd/labelmap_det.txt"

objName = ["background",
"aeroplane", "bicycle", "bird", "boat",
"bottle", "bus", "car", "cat", "chair",
"cow", "diningtable", "dog", "horse",
"motorbike", "person", "pottedplant",
"sheep", "sofa", "train", "tvmonitor"]


def process(image, out):
    h, w, _ = image.shape
    for detection in out[0, 0, :, :]:
        score = float(detection[2])
        index = int(detection[1])
        word = "score:%.2f, %s" % (score, objName[index])
        if 0.5 < score:
            left = detection[3] * w
            top = detection[4] * h
            right = detection[5] * w
            bottom = detection[6] * h
            cv.rectangle(image, (int(left), int(top)), (int(right), int(bottom)), (255, 0, 0), 2)
            cv.putText(image, word, (int(left) - 10, int(top) - 5), cv.FONT_HERSHEY_SIMPLEX, 0.7,
                       (0, 255, 0), 2, cv.LINE_8)
            print(word)
    return image


def main():
    video = cv.VideoCapture("../../../raspberry-auto/pic/two_red_line.mp4")
    net = cv.dnn.readNetFromCaffe(ssd_config, ssd_bin)
    while True:
        ret, frame = video.read()
        if False is ret:
            break
        data = cv.dnn.blobFromImage(frame, 0.007843, (300, 300), (127.5, 127.5, 127.5), True, False)
        net.setInput(data)
        out = net.forward()
        result = process(frame, out)
        cv.imshow("video-ssd-demo", result)
        key = cv.waitKey(10)
        if 27 == key:
            print("exit.")
            break
    print("main is end")


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()