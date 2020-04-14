#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
OpenCV DNN单张与多张图像的推断

    OpenCV DNN中支持单张图像推断，同时还支持分批次方式的图像推断，对应的两个相关API分别为blobFromImage与blobFromImages，它们的返回对象都
是一个四维的Mat对象-按照顺序分别为NCHW 其组织方式如下：
N表示多张图像
C表示接受输入图像的通道数目
H表示接受输入图像的高度
W表示接受输入图像的宽度
"""

bin_model = "../../../raspberry-auto/models/googlenet/bvlc_googlenet.caffemodel"
config = "../../../raspberry-auto/models/googlenet/bvlc_googlenet.prototxt"
txt = "../../../raspberry-auto/models/googlenet/classification_classes_ILSVRC2012.txt"


def main():
    net = cv.dnn.readNetFromCaffe(config, bin_model)
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)
    classes = None
    with open(txt, "r") as f:
        classes = f.read().rstrip("\n").split("\n")
    images = [cv.imread("../../../raspberry-auto/pic/70eb501cjw1dwp7pecgewj.jpg"),
              cv.imread("../../../raspberry-auto/pic/Meter_in_word.png"),
              cv.imread("../../../raspberry-auto/pic/hw_freebuds3_2.jpg")]
    data = cv.dnn.blobFromImages(images, 1.0, (224, 224), (104, 117, 123), False, crop=False)
    net.setInput(data)
    outs = net.forward()
    t, _ = net.getPerfProfile()
    text = "Inference time: %.2f ms" % (t * 1000.0 / cv.getTickFrequency())
    print(text)
    for i in range(len(outs)):
        out = outs[i]
        class_id = int(np.argmax(out))
        confidence = out[class_id]
        cv.putText(images[i], text, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
        label = "%s: %.4f" % (classes[class_id] if classes else "Class #%d" % class_id, confidence)
        cv.putText(images[i], label, (50, 50), cv.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)
        cv.imshow("googlenet demo", images[i])
        cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
