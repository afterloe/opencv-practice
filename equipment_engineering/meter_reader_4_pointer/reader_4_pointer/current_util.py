#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import numpy as np


TEMP_VALUE_LIST = []
CONFIDENCE = 45


def mean_shift_filtering(value):
    TEMP_VALUE_LIST.append(value)
    if 20 > len(TEMP_VALUE_LIST):
        del TEMP_VALUE_LIST[0]
    mean = np.mean(TEMP_VALUE_LIST)
    reliability = np.sqrt((value - mean) ** 2)
    if CONFIDENCE < (reliability / mean) * 100:
        return TEMP_VALUE_LIST[len(TEMP_VALUE_LIST) - 1]
    return value


def avg_circles(circles, b):
    avg_x, avg_y, avg_r = 0, 0, 0
    for i in range(b):
        avg_x = avg_x + circles[0][i][0]
        avg_y = avg_y + circles[0][i][1]
        avg_r = avg_r + circles[0][i][2]
    return int(avg_x / b), int(avg_y / b), int(avg_r / b)


def calculate_distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def is_number(input_str):
    try:
        float(input_str)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(input_str)
        return True
    except (TypeError, ValueError):
        pass

    return False
