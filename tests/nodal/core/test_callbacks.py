#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase

import nodal
from nodal.core import Callbacks


class TestCallbacks(TestCase):

    def callback_func(self, node):
        return node

    def noop_callback_func(self, node):
        return node

    def on_create_callback_func(self, node):
        self._nodes.append(node)

    def on_destroy_callback_func(self, node):
        if node not in self._nodes:
            return
        self._nodes.remove(node)

    def setUp(self):
        Callbacks.clear()
        self._nodes = []

    def test_clear(self):
        Callbacks.add_on_create(self.callback_func)
        Callbacks.add_on_destroy(self.callback_func)
        Callbacks.clear()
        self.assertFalse(Callbacks._callbacks['on_create'])
        self.assertFalse(Callbacks._callbacks['on_destroy'])

    def test__add_callback(self):
        self.assertRaises(
            AttributeError,
            Callbacks._add_callback, 'foo', self.callback_func
        )

    def test__trigger(self):
        noop = nodal.nodes.NoOp()
        self.assertRaises(AttributeError, Callbacks._trigger, 'foo', noop)

        def noop_rename(node):
            node.name += '_foo'

        Callbacks.add_on_create(noop_rename, node_classes=['NoOp'])

        noop = nodal.nodes.NoOp()
        self.assertTrue(noop.name.endswith('_foo'))

        plus = nodal.nodes.Plus()
        self.assertFalse(plus.name.endswith('_foo'))

    def test_add_on_create(self):
        on_create = Callbacks._callbacks['on_create']
        Callbacks.add_on_create(self.callback_func)
        self.assertTrue(self.callback_func in on_create[None])

        Callbacks.add_on_create(self.noop_callback_func, ['NoOp'])
        self.assertTrue(self.noop_callback_func in on_create['NoOp'])

    def test_add_on_destroy(self):
        on_destroy = Callbacks._callbacks['on_destroy']
        Callbacks.add_on_destroy(self.callback_func)
        self.assertTrue(self.callback_func in on_destroy[None])

        Callbacks.add_on_destroy(self.noop_callback_func, ['NoOp'])
        self.assertTrue(self.noop_callback_func in on_destroy['NoOp'])

    def test_trigger_on_create(self):
        Callbacks.add_on_create(self.on_create_callback_func)
        noop = nodal.nodes.NoOp()
        self.assertTrue(noop in self._nodes)

    def test_trigger_on_destroy(self):
        Callbacks.add_on_create(self.on_create_callback_func)
        Callbacks.add_on_destroy(self.on_destroy_callback_func)
        noop = nodal.nodes.NoOp()
        self.assertTrue(noop in self._nodes)
        noop.delete()
        self.assertFalse(noop in self._nodes)
