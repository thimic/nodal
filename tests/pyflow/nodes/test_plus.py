#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase

import pyflow


class TestPlus(TestCase):

    def test_multi_input(self):
        plus1 = pyflow.nodes.Plus(1)
        plus2 = pyflow.nodes.Plus(2)
        plus3 = pyflow.nodes.Plus(3)
        plus4 = pyflow.nodes.Plus(4)

        plus4.set_input(0, plus1)
        plus4.set_input(1, plus2)
        plus4.set_input(2, plus3)

        self.assertEqual(plus4.result, 10)

        plus10 = pyflow.nodes.Plus(10)
        plus1.set_input(0, plus10)
        self.assertEqual(plus4.result, 20)

        plus5 = pyflow.nodes.Plus(5)
        plus1.set_input(1, plus5)
        self.assertEqual(plus4.result, 25)
