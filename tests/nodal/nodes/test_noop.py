#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nodal

from nodal.core import MaxInputsExceededException

from unittest import TestCase


class TestNoOp(TestCase):

    def test_input(self):
        noop1 = nodal.nodes.NoOp()
        noop2 = nodal.nodes.NoOp()
        noop2.set_input(0, noop1)

        self.assertRaises(MaxInputsExceededException, noop1.input, 1)
        self.assertIsNone(noop1.input(0))
        self.assertEqual(noop1, noop2.input(0))

        self.assertIn(noop2, noop1.dependents)
        self.assertTrue(noop2.set_input(0, None))
        self.assertIsNone(noop2.input(0))
        self.assertFalse(noop1.dependents)

    def test_set_input(self):
        noop1 = nodal.nodes.NoOp()
        noop2 = nodal.nodes.NoOp()
        self.assertRaises(MaxInputsExceededException, noop1.set_input, 1, noop2)
        self.assertTrue(noop1.set_input(0, noop2))

    def test_output_type(self):
        noop = nodal.nodes.NoOp()
        self.assertEqual(object, noop.output_type)

    def test__execute(self):
        plus = nodal.nodes.Plus(5)
        noop = nodal.nodes.NoOp()

        self.assertEqual(noop.result, [])

        noop.set_input(0, plus)
        noop.execute()
        self.assertEqual(5, noop.result)

