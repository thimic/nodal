#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase

import nodal

from nodal import Graph


class TestGraph(TestCase):

    def setUp(self):
        self.graph = Graph()

    def tearDown(self):
        self.graph.clear()

    def test_create_node(self):
        noop = self.graph.create_node('NoOp')
        self.assertTrue(noop in self.graph.nodes)

        output = nodal.nodes.Output()
        self.assertTrue(output in self.graph.nodes)

    def test_delete_node(self):
        noop = self.graph.create_node('NoOp')
        self.assertTrue(noop in self.graph.nodes)
        self.graph.delete_node(noop)
        self.assertFalse(self.graph.nodes)

        output = nodal.nodes.Output()
        self.assertTrue(output in self.graph.nodes)
        output.delete()
        self.assertFalse(self.graph.nodes)

    def test_nodes(self):
        self.assertFalse(self.graph.nodes)
        noop = self.graph.create_node('NoOp')
        self.assertListEqual(self.graph.nodes, [noop])

    def test_clear(self):
        noop = self.graph.create_node('NoOp')
        self.assertEqual(self.graph.nodes, [noop])
        self.graph.clear()
        self.assertFalse(self.graph.nodes)

    def test_execute(self):
        plus1 = self.graph.create_node('Plus')
        plus1.value = 5

        plus2 = nodal.nodes.Plus()
        plus2.value = 2
        plus2.set_input(0, plus1)

        output = self.graph.create_node('Output')
        output.set_input(0, plus2)

        result = self.graph.execute([plus1, plus2, output])
        self.assertDictEqual(result, {plus1.name: 5, plus2.name: 7, output.name: 7})

    def test__on_node_create(self):
        noop1 = self.graph.create_node('NoOp')
        self.assertEqual(noop1.name, 'NoOp1')

        noop2 = nodal.nodes.NoOp()
        self.assertEqual(noop2.name, 'NoOp2')

        noop3 = self.graph.create_node('NoOp')
        self.assertEqual(noop3.name, 'NoOp3')

        output = nodal.nodes.Output()
        self.assertEqual(output.name, 'Output1')

    def test__on_node_destroy(self):

        # Create 3 NoOps
        noop1 = self.graph.create_node('NoOp')
        noop2 = nodal.nodes.NoOp()
        noop3 = self.graph.create_node('NoOp')

        # Delete two NoOps and check that we are left with one
        self.graph.delete_node(noop3)
        noop2.delete()
        self.assertEqual(self.graph.nodes, [noop1])

        # Create new NoOp and check that it gets named as expected
        noop2 = nodal.nodes.NoOp()
        self.assertEqual(noop2.name, 'NoOp2')
