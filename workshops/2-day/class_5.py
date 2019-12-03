#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np
import argparse

HEIGHT = 512
WIDTH = 512
THICKNESS = 1


class DrawChain(object):
    def __init__(self):
        self.successor = ''

    def set_successor(self, successor):
        self.successor = successor
        return successor

    def handle_request(self, command, canvas):
        pass


class DrawChainRectangle(DrawChain):
    def handle_request(self, command, canvas):
        if 1 != command['shape'] and 0 != command['shape']:
            return self.successor.handle_request(command, canvas)
        thickness = cv.FILLED if command['fill'] else THICKNESS
        cv.rectangle(canvas, generatorPointer(), generatorPointer(), generatorColor(), thickness, cv.LINE_8)
        return canvas


class DrawChainCircle(DrawChain):
    def handle_request(self, command, canvas):
        if 2 != command['shape'] and 0 != command['shape']:
            return self.successor.handle_request(command, canvas)
        thickness = cv.FILLED if command['fill'] else THICKNESS
        r, _ = generatorPointer()
        cv.circle(canvas, generatorPointer(), r, generatorColor(), thickness, cv.LINE_8)
        return canvas


class DrawChainEllipse(DrawChain):
    def handle_request(self, command, canvas):
        if 3 != command['shape'] and 0 != command['shape']:
            return self.successor.handle_request(command, canvas)
        thickness = cv.FILLED if command['fill'] else THICKNESS
        cv.ellipse(canvas, generatorPointer(), generatorPointer(), 360, 0, 360, generatorColor(), thickness, cv.LINE_8)
        return canvas


class DrawChainAll(DrawChain):
    def handle_request(self, command, canvas):
        if 0 != command['shape']:
            return self.successor.handle_request(command, canvas)
        canvas = chain_rectangle.handle_request(command, canvas)
        canvas = chain_circle.handle_request(command, canvas)
        return chain_ellipse.handle_request(command, canvas)


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


def drawChain(canvas, command):
    canvas = chain_all.handle_request(command, canvas)
    cv.imshow("image", canvas)


# 接收参数
arg_map = initArg()
print(arg_map)
# 创建画布
mat = np.zeros(shape=(512, 512, 3), dtype=np.uint8)

# 初始化职责链
chain_all = DrawChainAll()
chain_rectangle = DrawChainRectangle()
chain_circle = DrawChainCircle()
chain_ellipse = DrawChainEllipse()

chain_all.set_successor(chain_rectangle).set_successor(chain_circle).set_successor(chain_ellipse)

if arg_map['loop']:
    for _ in range(100000):
        drawChain(canvas=mat, command=arg_map)
        input_key = cv.waitKey(20)
        if 27 == input_key:  # esc
            break
else:
    drawChain(canvas=mat, command=arg_map)
    cv.waitKey(0)

cv.destroyAllWindows()
