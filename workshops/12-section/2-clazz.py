#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
Opencv DNN 实现图像分类
    使用ImageNet数据集支持1000分类的GoogleNet网络模型，其中label标签是在一个单独的文本文件中读取
    
读取模型的API：
    cv.dnn.readNetFromCaffe(prototxt, caffeModel)
        - prototxt 模型配置文件
        - caffeModel 模型的权重二进制文件

使用模型实现预测的时候，需要读取图像作为输入，网络模型支持的输入数据是四维的输入，所以要把读取到的Mat对象转换为四维张量，OpenCV的提供的API如
下：
    cv.dnn.blobFromImage(image, scalefactor, size, mean, swapRB, crop, ddepth)
        - image 输入图像
        - scalefactor 缩放比列，默认1.0 
        - size 网络接受的数据大小
        - mean 训练时数据集的均值
        - swapRB 是否互换Red与Blur通道
        - crop 剪切
        - ddepth 数据类型
        
ps: (模型说明)[https://github.com/opencv/opencv/tree/master/samples/dnn]

OpenCV可以设置计算机后台与计算目标设备，相关API如下
    cv.dnn.setPreferableBackend(backendId)
        - backendId 后台计算id DNN_BACKEND_DEFAULT (DNN_BACKEND_INFERENCE_ENGINE)表示默认使用intel的预测推断库
    (需要下载安装Intel® OpenVINO™ toolkit， 然后重新编译OpenCV源码，在CMake时候enable该选项方可)， 可加速计算！
    DNN_BACKEND_OPENCV 一般情况都是使用opencv dnn作为后台计算
    
    cv.dnn.net.setPreferableTarget(targetId)
        - targetId 目标设备ID
        
常见的目标设备id如下：
    -	DNN_TARGET_CPU其中表示使用CPU计算，默认是的
    -	DNN_TARGET_OPENCL 表示使用OpenCL加速，一般情况速度都很扯
    -	DNN_TARGET_OPENCL_FP16 可以尝试
    -	DNN_TARGET_MYRIAD 树莓派上的

关系图
 |                        | DNN_BACKEND_OPENCV | DNN_BACKEND_INFERENCE_ENGINE | DNN_BACKEND_HALIDE |
*|------------------------|--------------------|------------------------------|--------------------|
*| DNN_TARGET_CPU         |                  + |                            + |                  + |
*| DNN_TARGET_OPENCL      |                  + |                            + |                  + |
*| DNN_TARGET_OPENCL_FP16 |                  + |                            + |                    |
*| DNN_TARGET_MYRIAD      |                    |                            + |                    |
*| DNN_TARGET_FPGA        |                    |                            + |                    |
"""

bin_model = "../../../raspberry-auto/models/googlenet/bvlc_googlenet.caffemodel"
prototxt = "../../../raspberry-auto/models/googlenet/bvlc_googlenet.prototxt"
classes_path = "../../../raspberry-auto/models/googlenet/classification_classes_ILSVRC2012.txt"


def main():
    classes = None
    with open(classes_path, "rt") as f:
        classes = f.read().rstrip("\n").split("\n")
    net = cv.dnn.readNetFromCaffe(prototxt, bin_model)
    image = cv.imread("../../../raspberry-auto/pic/Meter.jpg")
    blob = cv.dnn.blobFromImage(image, 1.0, (224, 224), (104, 117, 123), False, crop=False)
    result = np.copy(image)
    cv.imshow("src", image)
    net.setInput(blob)
    # 设置目标设备ID与后台计算ID
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    # 默认为CPU计算，且不进行后台计算ID设置
    net.setPreferableTarget(cv.dnn.DNN_TARGET_OPENCL)

    out = net.forward()
    out = out.flatten()
    classId = np.argmax(out)
    confidence = out[classId]
    t, _ = net.getPerfProfile()
    label = "Inference time: %.2f ms" % (t * 1000.0 / cv.getTickFrequency())
    print(label)
    cv.putText(result, label, (0, 15), cv.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, (255, 0, 0))
    label = "%s: %.4f" % (classes[classId] if classes else "Class #%d" % classId, confidence)
    print(label)
    cv.putText(result, label, (0, 50), cv.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.75, (0, 0, 255), 2)
    cv.imshow("result", result)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
