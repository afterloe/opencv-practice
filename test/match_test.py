#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import math


def t(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def main():
    width = pow(abs(7 - 4), 2)
    height = pow(abs(14 - 18), 2)
    hypotenuse = math.sqrt(width + height)
    print(width, height, hypotenuse)
    v = [0 for x in range(40)]
    print(v)
    v[39] = 99
    print(v)
    p = range(0, 40)
    print(p)
    print(t(0, 3, 4, 0))


if "__main__" == __name__:
    main()
