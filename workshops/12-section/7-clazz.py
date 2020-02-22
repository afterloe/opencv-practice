#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
OpenCV DNN 直接调用tensorflow的导出模型
    OpenCV在DNN模块中支持直接调用tensorflow object detection训练导出的模型使用，支持的模型包括
        - SSD
        - Faster-RCNN
        - Mask-RCNN

    三种经典的对象检测网络，这样就可以实现从tensorflow模型训练、导出模型、在OpenCV DNN调用模型网络实现自定义对象检测的技术链路，具有非常高
的实用价值。以Faster-RCNN为例.
(模型下载地址)[https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md]
    对于这些模型没有与之匹配的graph.pbtxt文件，OpenCV DNN模块提供python脚本来生成，相关详细说明看
(文章)[https://mp.weixin.qq.com/s/YZeCNjlVKTU6lOVrmYLDCQ]
"""

bin_model = "../../../raspberry-auto/models/ssd/frozen_inference_graph.pb"
pbtxt = "../../../raspberry-auto/models/ssd/graph.pbtxt"
label_map = "../../../raspberry-auto/models/ssd/mscoco_label_map.pbtxt"


def main():
    image = cv.imread("../../../raspberry-auto/pic/2020-17-08-27-19.jpeg")
    dnn = cv.dnn.readNetFromTensorflow(bin_model, pbtxt)
    h, w = image.shape[:2]
    data = cv.dnn.blobFromImage(image, 1.25, (300, 300), False, False)
    dnn.setInput(data)
    out = dnn.forward()
    for detection in out[0, 0, :, :]:
        score = float(detection[2])
        if 0.5 < score:
            # print(detection[1])  # label index
            left = int(detection[3] * w)
            top = int(detection[4] * h)
            right = int(detection[5] * w)
            bottom = int(detection[6] * h)
            cv.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 2)
    cv.imshow("result", image)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
