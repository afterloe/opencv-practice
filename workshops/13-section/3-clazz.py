#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
OpenCV DNN支持ENet网络模型的图像分割
    采用预先训练的ENet网络模型(下载地址)[https://github.com/e-lab/ENet-training], 基于Cityscapes数据集的训练预测结果。
该模型是torch模型，加载的API为：

cv.dnn.readNetFromTorch(model, isBinary)
    - model参数表示二进制的模型权重文件
    - isBinary 是否为二进制文件，默认为true

ps: 跑ENet网络的时候，OpenCV4.0.x与DLIE一起编译之后，当使用DNN_BACKEND_INFERENCE_ENGINE，作为推断后台的时候，会得到上采样最大池化
错误，切换为DNN_BACKEND_OPENCV 则能正常加载。
"""

model_bin = "../../../raspberry-auto/models/enet/model-best.net"
model_config = "../../../raspberry-auto/models/enet/enet-classes.txt"


def main():
    image = cv.imread("../../../raspberry-auto/pic/cityscapes_test.jpg")
    net = cv.dnn.readNetFromTorch(model_bin)
    data = cv.dnn.blobFromImage(image, 0.00392, (1024, 512), (0, 0, 0), True, False)
    cv.imshow("input", image)
    net.setInput(data)
    out = net.forward()
    t, _ = net.getPerfProfile()
    txt = "Inference time: %.2f ms" % (t * 1000.0 / cv.getTickFrequency())
    print(out.shape)
    color_lut = []
    n, con, h, w = out.shape
    for i in range(con):
        b = np.random.randint(0, 256)
        g = np.random.randint(0, 256)
        r = np.random.randint(0, 256)
        color_lut.append((b, g, r))
    max_cl = np.zeros((h, w), dtype=np.int32)
    max_val = np.zeros((h, w), dtype=np.float32)

    for i in range(con):
        for row in range(h):
            for col in range(w):
                t = max_val[row, col]
                s = out[0, i, row, col]
                if s > t:
                    max_val[row, col] = s
                    max_cl[row, col] = i

    segm = np.zeros((h, w, 3), dtype=np.uint8)
    for row in range(h):
        for col in range(w):
            index = max_cl[row, col]
            segm[row, col] = color_lut[index]

    h, w = image.shape[:2]
    segm = cv.resize(segm, (w, h), None, 0, 0, cv.INTER_NEAREST)
    print(segm.shape, image.shape)
    image = cv.addWeighted(image, 0.2, segm, 0.8, 0.0)
    cv.putText(image, txt, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
    cv.imshow("ENet demo", image)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
