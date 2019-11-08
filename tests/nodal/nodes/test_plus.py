#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nodal

from unittest import TestCase


class TestPlus(TestCase):

    def test_multi_input(self):
        plus1 = nodal.nodes.Plus(1)
        plus2 = nodal.nodes.Plus(2)
        plus3 = nodal.nodes.Plus(3)
        plus4 = nodal.nodes.Plus(4)

        plus4.set_input(0, plus1)
        plus4.set_input(1, plus2)
        plus4.set_input(2, plus3)

        self.assertEqual(plus4.result, 10)

        plus10 = nodal.nodes.Plus(10)
        plus1.set_input(0, plus10)
        self.assertEqual(plus4.result, 20)

        plus5 = nodal.nodes.Plus(5)
        plus1.set_input(1, plus5)
        self.assertEqual(plus4.result, 25)

    def test_disconnect_on_none_input(self):

        plus1 = nodal.nodes.Plus(1)
        plus2 = nodal.nodes.Plus(2)

        plus2.set_input(0, plus1)
        self.assertEqual(plus2.input(0), plus1)

        plus2.set_input(0, None)
        self.assertIsNone(plus2.input(0))

    def test_dirty(self):
        plus1 = nodal.nodes.Plus(1)
        self.assertTrue(plus1.dirty)
        plus1.execute()
        self.assertFalse(plus1.dirty)
        plus1.value = 2
        self.assertTrue(plus1.dirty)
        plus1.execute()
        plus1.value = 2
        self.assertFalse(plus1.dirty)
