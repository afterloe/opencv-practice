#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import unittest
from unittest.mock import patch


class Calculator(object):
    def add(self, a, b):
        return a+b


class TestProducer(unittest.TestCase):

    def setUp(self):
        self.calculator = Calculator()

    @patch.object(Calculator, 'add')
    def test_add(self, mock_add):
        mock_add.return_value = 3
        print("111111111")
        self.assertEqual(self.calculator.add(8, 14), 3)


if "__main__" == __name__:
    unittest.main()
