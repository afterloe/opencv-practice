#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import math


def main():
    width = pow(abs(7 - 4), 2)
    height = pow(abs(14 - 18), 2)
    hypotenuse = math.sqrt(width + height)
    print(width, height, hypotenuse)


if "__main__" == __name__:
    main()
