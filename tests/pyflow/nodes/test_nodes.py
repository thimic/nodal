#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyflow

from pyflow.core import NodeClassNotFoundException

from unittest import TestCase


class TestNodes(TestCase):

    def test_nodes_getattr(self):

        noop = pyflow.nodes.NoOp()
        self.assertTrue(noop)
        self.assertRaises(
            NodeClassNotFoundException,
            getattr, pyflow.nodes, 'Foo'
        )
