#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
OpenCV DNN 图像颜色化模型使用 
    OpenCV DNN在4.0支持灰度图像的彩色化模型,根据2016年ECCV的论文基于卷积神经网络模型，通过对Lab色彩空间进行量化分割，映射到最终的CNN输出
结果，最后转换为RGB彩色图像.

论文[https://arxiv.org/pdf/1603.08511.pdf]
模型下载[https://github.com/richzhang/colorization]

ps: OpenCV DNN使用该模型时候，除了正常的Caffe模型与配置文件之外，还需要一个Lab的量化表。该表在github上可以进行下载，位于resources下
"""

model_txt = "../../../raspberry-auto/models/colorization/colorization_deploy_v2.prototxt"
model_bin = "../../../raspberry-auto/models/colorization/colorization_release_v2.caffemodel"
pts_txt = "../../../raspberry-auto/models/colorization/pts_in_hull.npy"
W_in = 224
H_in = 224


def main():
    # 加载DNN颜色转换模型
    net = cv.dnn.readNetFromCaffe(model_txt, model_bin)
    # 加载Lab量化表，用于集群中心设置
    pts_in_hull = np.load(pts_txt)
    # 设置成2行313列，卷积核为1*1 若不进行设置，在图像转换时会出现异常
    pts_in_hull = pts_in_hull.transpose().reshape(2, 313, 1, 1)
    net.getLayer(net.getLayerId("class8_ab")).blobs = [pts_in_hull.astype(np.float32)]
    net.getLayer(net.getLayerId("conv8_313_rh")).blobs = [np.full([1, 313], 2.606, np.float32)]
    image = cv.imread("G:\\Project\\opencv-ascs-resources\\d788d43f8794a4c2e3aee3470cf41bd5ac6e39c8.jpg")
    h, w = image.shape[:2]
    img_rgb = (image[:, :, [2, 1, 0]] * 1.0 / 255).astype(np.float32)
    img_lab = cv.cvtColor(img_rgb, cv.COLOR_RGB2Lab)
    img_l = img_lab[:, :, 0]
    (H_orig, W_orig) = img_rgb.shape[:2]
    img_rs = cv.resize(img_rgb, (W_in, H_in))
    img_lab_rs = cv.cvtColor(img_rs, cv.COLOR_RGB2Lab)
    # 设置图像的L通道
    img_l_rs = img_lab_rs[:, :, 0]
    img_l_rs -= 50
    net.setInput(cv.dnn.blobFromImage(img_l_rs))
    ab_dec = net.forward()[0, :, :, :].transpose((1, 2, 0))
    (H_out, W_out) = ab_dec.shape[:2]
    ab_dec_us = cv.resize(ab_dec, (W_orig, H_orig))
    img_lab_out = np.concatenate((img_l[:, :, np.newaxis], ab_dec_us), axis=2)
    img_bgr_out = np.clip(cv.cvtColor(img_lab_out, cv.COLOR_Lab2BGR), 0, 1)
    frame = cv.resize(image, (w, h))
    cv.imshow('origin', frame)
    cv.imshow('gray', cv.cvtColor(frame, cv.COLOR_RGB2GRAY))
    cv.normalize(img_bgr_out, img_bgr_out, 0, 255, cv.NORM_MINMAX)
    cv.imshow('colorized', cv.resize(np.uint8(img_bgr_out), (w, h)))
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
