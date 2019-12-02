#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np
import argparse

HEIGHT = 512
WIDTH = 512
THICKNESS = 1


def initArg():
    ap = argparse.ArgumentParser()
    ap.description = "opencv draw by afterloe version 1.0.0"
    ap.add_argument("-f", "--fill", type=bool, default=False, help="bool, True or False；表明绘制内容是否填充")
    ap.add_argument("-l", "--loop", type=bool, default=False, help="bool, True or False; 表明是否进行循环演示")
    ap.add_argument("-s", "--shape", type=int, default=0,
                    help="0, 1, 2, 3; 0 - 全部绘制、 1 - 只绘制矩形、 2 - 只绘制圆形、 3 - 只绘制椭圆")
    return vars(ap.parse_args())


def generatorColor():
    b = np.random.randint(0, 256)
    g = np.random.randint(0, 256)
    r = np.random.randint(0, 256)
    return b, g, r


def generatorPointer():
    x = np.random.rand() * WIDTH
    y = np.random.rand() * HEIGHT
    return np.int(x), np.int(y)


def drawRectangle(canvas, command):
    if 1 != command['shape'] and 0 != command['shape']:
        return False, command, canvas
    thickness = cv.FILLED if command['fill'] else THICKNESS
    x, y = generatorPointer()
    x1, y1 = generatorPointer()
    b, g, r = generatorColor()
    print("draw rectangle (%d, %d) rgb is (%d, %d, %d) width is %d" % (x, y, r, g, b, thickness))
    cv.rectangle(canvas, (x, y), (x1, y1), (b, g, r), thickness, cv.LINE_8)
    return True, command, canvas


def drawCircle(canvas, command):
    if 2 != command['shape'] and 0 != command['shape']:
        return False, command, canvas
    thickness = cv.FILLED if command['fill'] else THICKNESS
    r, _ = generatorPointer()
    x, y = generatorPointer()
    b, g, r = generatorColor()
    cv.circle(canvas, (x, y), r, (b, g, r), thickness, cv.LINE_8)
    return True, command, canvas


def drawEllipse(canvas, command):
    if 3 != command['shape'] and 0 != command['shape']:
        return False, command, canvas
    thickness = cv.FILLED if command['fill'] else THICKNESS
    x, y = generatorPointer()
    x1, y1 = generatorPointer()
    b, g, r = generatorColor()
    cv.ellipse(canvas, (x, y), (x1, y1), 360, 0, 360, (b, g, r), thickness, cv.LINE_8)
    return True, command, canvas


def drawAll(canvas, command):
    if 0 != command['shape']:
        return False, command, canvas
    _, _, canvas = drawRectangle(canvas, command)
    _, _, canvas = drawCircle(canvas, command)
    _, _, canvas = drawEllipse(canvas, command)
    return True, command, canvas


def drawChain(canvas, command):
    flag, _, canvas = drawAll(canvas, command)
    if not flag:
        _, _, canvas = drawRectangle(canvas, command)
        _, _, canvas = drawCircle(canvas, command)
        _, _, canvas = drawEllipse(canvas, command)
    cv.imshow("image", canvas)


# 接收参数
arg_map = initArg()
print(arg_map)
# 创建画布
mat = np.zeros(shape=(512, 512, 3), dtype=np.uint8)
if arg_map['loop']:
    for _ in range(100000):
        drawChain(mat, arg_map)
        input_key = cv.waitKey(20)
        if 27 == input_key:  # esc
            break
else:
    drawChain(mat, arg_map)
    cv.waitKey(0)

cv.destroyAllWindows()
