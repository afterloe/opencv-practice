#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv

"""
OpenCV DNN 调用openpose模型实现姿态评估

OpenCV DNN模块中使用openopse的深度学习模型,实现人体单人姿态评估, 首先需要下载人体姿态评估的预训练模型。
基于COCO数据集训练的模型下载地址如下：
http://posefs1.perception.cs.cmu.edu/OpenPose/models/pose/coco/pose_iter_440000.caffemodel
https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/openpose_pose_coco.prototxt


基于MPI数据集训练的模型下载地址如下：
http://posefs1.perception.cs.cmu.edu/OpenPose/models/pose/mpi/pose_iter_160000.caffemodel
https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/openpose_pose_mpi_faster_4_stages.prototxt

手势姿态模型
http://posefs1.perception.cs.cmu.edu/OpenPose/models/hand/pose_iter_102000.caffemodel
https://raw.githubusercontent.com/CMU-Perceptual-Computing-Lab/openpose/master/models/hand/pose_deploy.prototxt

其中COCO模型会生成18个点，MPI模型生成14个点，手势姿态模型生成20个点，根据这些点可以绘制出人体的关键节点或者手的关键节点。OpenCV DNN支持的姿态评估都是基于预训练的Caffe模型，而且模型没有经过专门的优化处理，速度特别的慢，在CPU上基本是秒级别才可以出结果，离实时运行差好远，但是对一些静态的手势分析还是有一定的帮助与作用。
代码实现可以分为如下几个步骤
1.	加载网络
2.	获取heatmap数据，根据heatmap寻找最大score与位置信息
3.	根据位置信息，绘制连接直线
"""

bin_model = "../../../raspberry-auto/models/openpose/coco_pose_iter.caffemodel"
config = "../../../raspberry-auto/models/openpose/coco_pose_deploy.prototxt"


def main():
    BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                   "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                   "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
                   "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

    POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
                   ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
                   ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
                   ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
                   ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]
    image = cv.imread("../../../raspberry-auto/pic/hand.jpg")
    dnn = cv.dnn.readNetFromCaffe(config, bin_model)
    h, w = image.shape[:2]
    data = cv.dnn.blobFromImage(image, 1.0 / 255, (224, 224), (104, 117, 123), False, False)
    dnn.setInput(data)
    out = dnn.forward()

    points = []
    for i in range(len(BODY_PARTS)):
        heat_map = out[0, i, :, :]
        _, conf, _, point = cv.minMaxLoc(heat_map)
        x = (w * point[0]) / out.shape[3]
        y = (h * point[1]) / out.shape[2]
        points.append((int(x), int(y)))
    for pair in POSE_PAIRS:
        part_from = pair[0]
        part_to = pair[1]
        assert(part_from in BODY_PARTS)
        assert(part_to in BODY_PARTS)
        id_from = BODY_PARTS[part_from]
        id_to = BODY_PARTS[part_to]
        if points[id_from] and points[id_to]:
            cv.line(image, points[id_from], points[id_to], (0, 255, 0), 3)
            cv.ellipse(image, points[id_from], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
            cv.ellipse(image, points[id_to], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
    t, _ = dnn.getPerfProfile()
    freq = cv.getTickFrequency() / 1000
    cv.putText(image, "%.2f ms" % (t / freq), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
    cv.imshow("dst", image)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
