#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase

import pyflow
from pyflow.core import Callbacks


class TestCallbacks(TestCase):

    def callback_func(self, node):
        return node

    def noop_callback_func(self, node):
        return node

    def on_create_callback_func(self, node):
        self._nodes.append(node)

    def setUp(self):
        Callbacks.clear()
        self._nodes = []

    def test_clear(self):
        Callbacks.add_on_create(self.callback_func)
        Callbacks.clear()
        self.assertFalse(Callbacks._on_create)

    def test_add_on_create(self):
        Callbacks.add_on_create(self.callback_func)
        self.assertTrue(self.callback_func in Callbacks._on_create[None])

        Callbacks.add_on_create(self.noop_callback_func, ['NoOp'])
        self.assertTrue(self.noop_callback_func in Callbacks._on_create['NoOp'])

    def test_trigger_on_create(self):
        Callbacks.add_on_create(self.on_create_callback_func)
        noop = pyflow.nodes.NoOp()
        self.assertTrue(noop in self._nodes)
