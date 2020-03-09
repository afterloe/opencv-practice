#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import unittest.mock


class Calculator:
    def sum(self, a, b):
        return a + b


class CoreTest(unittest.TestCase):

    def setUp(self):
        self.calc = Calculator()

    def test_f2(self):
        answer = self.calc.sum(2, 4)
        self.assertEqual(answer, 6)


if "__main__" == __name__:
    unittest.main()
