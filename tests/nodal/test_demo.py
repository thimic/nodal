#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nodal import demo

from unittest import TestCase


class TestDemo(TestCase):

    def test_demo(self):
        self.assertIsNone(demo.demo())
