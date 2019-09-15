#!/usr/bin/env python3
from unittest import skip, TestCase

import pyflow

from pyflow import Graph
from pyflow.core import Callbacks


# -*- coding: utf-8 -*-
class TestGraph(TestCase):

    def setUp(self):
        self.graph = Graph()

    def test_create_node(self):
        noop = self.graph.create_node('NoOp')
        self.assertTrue(noop in self.graph.nodes)

        output = pyflow.nodes.Output()
        self.assertTrue(output in self.graph.nodes)

    def test_nodes(self):
        self.assertFalse(self.graph.nodes)
        noop = self.graph.create_node('NoOp')
        self.assertListEqual(self.graph.nodes, [noop])

    @skip('Not yet implemented')
    def test_execute(self):
        self.fail()

    def test__on_node_create(self):
        noop1 = self.graph.create_node('NoOp')
        self.assertEqual(noop1.name, 'NoOp1')

        noop2 = pyflow.nodes.NoOp()
        self.assertEqual(noop2.name, 'NoOp2')

        noop3 = self.graph.create_node('NoOp')
        self.assertEqual(noop3.name, 'NoOp3')

        output = pyflow.nodes.Output()
        self.assertEqual(output.name, 'Output1')
