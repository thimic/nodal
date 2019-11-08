#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nodal

from nodal.core import NodeClassNotFoundException

from unittest import TestCase


class TestNodes(TestCase):

    def test_nodes_getattr(self):

        noop = nodal.nodes.NoOp()
        self.assertTrue(noop)
        self.assertRaises(
            NodeClassNotFoundException,
            getattr, nodal.nodes, 'Foo'
        )
