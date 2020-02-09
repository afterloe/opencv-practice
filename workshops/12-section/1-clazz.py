#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
DNN模块 - 获取导入模型各层描述信息
    模型支持1k个类别的图像分类，OpenCV DNN模块支持以下框架的预训练模型的前馈网络（预测图）使用
        - Caffe (*.caffemodel, http://caffe.berkeleyvision.org/)
        - TensorFlow (*.pb, https://www.tensorflow.org/)
        - Torch (*.net / *.t7, http://torch.ch/)
        - DLDT (*.bin, https://software.intel.com/openvino-toolkit)
        - Darknet (*.weights, https://pjreddie.com/darknet/)
    针对其模型的二进制描述文件，不同的框架配置命也不一样
        - Caffe (*.prototxt, http://caffe.berkeleyvision.org/)
        - TensorFlow (*.pbtxt, https://www.tensorflow.org/)
        - Darknet (*.cfg, https://pjreddie.com/darknet/)
        - DLDT (*.xml, https://software.intel.com/openvino-toolkit)
        
DNN 读取模型的API描述如下
    cv.dnn.readNet(model, config, framework)
        - model 二进制训练好的权重文件, 如上描述
        - config 权重文件的描述信息， 如上描述
        - framework 框架名（可舍），说明模型由哪个框架训练得出的
"""


def main():
    bin_model = "../../../raspberry-auto/models/googlenet/bvlc_googlenet.caffemodel"
    protxt = "../../../raspberry-auto/models/googlenet/bvlc_googlenet.prototxt"
    net = cv.dnn.readNet(bin_model, protxt)
    layer_name = net.getLayerNames()
    print(layer_name)
    for name in layer_name:
        index = net.getLayerId(name)
        layer = net.getLayer(index)
        print("layer id: %d, type: %s, name: %s" % (index, layer.type, layer.name))
    print("successfully loaded all model")


if "__main__" == __name__:
    main()
