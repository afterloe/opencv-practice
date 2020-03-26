#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from unittest import TestCase
from ..reader_4_pointer.current_util import *


class TestCurrentUtil(TestCase):

    def test_mean_shift_filtering(self):
        value = [0.045, 0.207, 0.028, 0.039, 0.220, 0.210, 0.077, 0.078, 0.078, 0.044, 0.208, 0.207, 0.076,
                 0.160, 0.078, 0.207, 0.207, 0.211, 0.211, 0.053, 0.0716]
        print(len(value))
        for v in value:
            current_value = mean_shift_filtering(v)
            print(current_value)

    def test_print_value(self):
        print("%s %.2f%%" % ("afterloe", 0.36 * 100.0))
