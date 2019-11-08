#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nodal

from unittest import TestCase


class TestText(TestCase):

    def test__execute(self):
        text1 = nodal.nodes.Text('Hello')
        self.assertEqual(text1.execute(), 'Hello')

        text2 = nodal.nodes.Text('World')
        self.assertEqual(text2.execute(), 'World')

        text2.set_input(0, text1)
        self.assertEqual(text2.execute(), 'Hello World')

    def test_text(self):
        text1 = nodal.nodes.Text('Hello')
        self.assertEqual(text1.text, 'Hello')
        text1.execute()
        self.assertFalse(text1.dirty)

        text1.text += ' World!'
        self.assertEqual(text1.text, 'Hello World!')
        self.assertTrue(text1.dirty)
        text1.execute()

        text1.text = 'Hello World!'
        self.assertFalse(text1.dirty)


