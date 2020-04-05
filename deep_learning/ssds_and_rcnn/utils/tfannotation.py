#!/usr/bin/env python3
# -*- coding=utf-8 -*-

# 引入 tensorflow object detector api数据集处理函数
from object_detection.utils.dataset_util import bytes_list_feature, float_list_feature, int64_list_feature
from object_detection.utils.dataset_util import int64_feature, bytes_feature


class TFAnnotation(object):

    def __init__(self):
        # 分别存储边界框的（x，y）坐标。
        # textLabels列表是每个边界框的人类可读类标签的列表。
        self.x_mins = []
        self.x_maxs = []
        self.y_mins = []
        self.y_maxs = []
        self.text_labels = []
        self.classes = []
        self.difficult = []
        # 存储TensorFlow编码的图像及其宽度，高度，图像编码类型和文件名
        self.image = None
        self.width = None
        self.height = None
        self.encoding = None
        self.filename = None

    def build(self):
        w = int64_feature(self.width)
        h = int64_feature(self.height)
        filename = bytes_feature(self.filename.encode("utf8"))
        encoding = bytes_feature(self.encoding.encode("utf8"))
        image = bytes_feature(self.image)
        x_mins = float_list_feature(self.x_mins)
        x_maxs = float_list_feature(self.x_maxs)
        y_mins = float_list_feature(self.y_mins)
        y_maxs = float_list_feature(self.y_maxs)
        text_labels = bytes_list_feature(self.text_labels)
        classes = int64_list_feature(self.classes)
        difficult = int64_list_feature(self.difficult)
        # 数据经 tf api调整后 开始构建 数据字典
        data = {
            "image/height": h,
            "image/width": w,
            "image/filename": filename,
            "image/source_id": filename,
            "image/encoded": image,
            "image/format": encoding,
            "image/object/bbox/xmin": x_mins,
            "image/object/bbox/xmax": x_maxs,
            "image/object/bbox/ymin": y_mins,
            "image/object/bbox/ymax": y_maxs,
            "image/object/class/text": text_labels,
            "image/object/class/label": classes,
            "image/object/difficult": difficult,
        }
        return data
