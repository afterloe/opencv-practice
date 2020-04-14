#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

"""
不支持音频编码与解码保存，不是一个音视频处理的库！主要是分析与解析视频内容。保存文件最大支持单个文件为2G，
超过2G后使用新的文件进行存储
"""
capture = cv.VideoCapture("../../out/resources/Megamind.avi")
# capture = cv.VideoCapture(0)
height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)  # 获取视频高度
width = capture.get(cv.CAP_PROP_FRAME_WIDTH)  # 获取视频宽度
frame = capture.get(cv.CAP_PROP_FRAME_COUNT)  # 获取视频帧数
fps = capture.get(cv.CAP_PROP_FPS)  # 获取视频的fps值

print("height: %d ,width: %d ,frame: %d ,fps: %d" % (height, width, frame, fps))

# 不知道是不是opencv的底层bug， 使用MP4命名进行文件保存会提示 FFMPEG: tag 0x58564944/'DIVX' is not supported,
# 但文件依旧能够保存， 若使用 *.avi 作为结尾，则不提示
"""
    path: 存储的路径
    fourcc: 编解码器， 可参考http://www.fourcc.org/codecs.php 进行， 使用divx比较常见
    fps： 顾名思义
    size: 视频的宽高
    isColor: 是否输出三通道彩色视频， 默认为True
"""
out = cv.VideoWriter("../../out/save.mp4", cv.VideoWriter_fourcc('D', 'I', 'V', 'X'), 15,
                     (np.int(width), np.int(height)), True)
while True:
    ret, frame = capture.read()
    if True is ret:
        cv.imshow("video-input", frame)
        out.write(frame)
        input_key = cv.waitKey(5)
        if 27 == input_key:  # esc
            break
    else:
        break

capture.release()
cv.destroyAllWindows()
