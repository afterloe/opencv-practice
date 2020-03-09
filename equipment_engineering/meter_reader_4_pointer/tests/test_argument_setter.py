#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from unittest import TestCase
# from unittest.mock import patch
import os
from ..reader_4_pointer import argument_helper


class TestArgumentHelper(TestCase):
    
    def setUp(self):
        if os.path.isfile(argument_helper.DEFAULT_CONFIG_SAVE_PATH):
            os.remove(argument_helper.DEFAULT_CONFIG_SAVE_PATH)
        self.helper = argument_helper.ArgumentHelper()

    def test_argument_1_getter(self):
        min_angle, max_angle, min_value, max_value = self.helper.getArgument()
        self.assertEqual(min_angle, 0)
        self.assertEqual(max_angle, 0)
        self.assertEqual(min_value, 0)
        self.assertEqual(max_value, 0)

    def test_argument_2_setter(self):
        self.helper.setArgument(45, 320, 0, 200)
        min_angle, max_angle, min_value, max_value = self.helper.getArgument()
        self.assertEqual(min_angle, 45)
        self.assertEqual(max_angle, 320)
        self.assertEqual(min_value, 0)
        self.assertEqual(max_value, 200)
        self.assertEqual(os.path.isfile(argument_helper.DEFAULT_CONFIG_SAVE_PATH), True)
        os.remove(argument_helper.DEFAULT_CONFIG_SAVE_PATH)
