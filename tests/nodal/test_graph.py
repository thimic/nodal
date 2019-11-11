#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase

import nodal

from nodal import Graph
from nodal.core.callbacks import Callbacks


class TestGraph(TestCase):

    def setUp(self):
        self.graph = Graph()

    def tearDown(self):
        self.graph.clear()
        Callbacks.clear()

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
        self.assertDictEqual(
            result,
            {plus1.name: 5, plus2.name: 7, output.name: 7}
        )

        self.assertEqual({plus1.name: 5}, self.graph.execute(plus1))

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

    def test_to_string(self):

        # Create graph
        plus1 = self.graph.create_node('Plus', 5)
        plus2 = self.graph.create_node('Plus', 10)
        plus3 = self.graph.create_node('Plus', 15)

        sum_ = self.graph.create_node('Plus')
        sum_.name = 'Sum1'
        sum_.set_input(0, plus1)
        sum_.set_input(1, plus2)
        sum_.set_input(2, plus3)

        output1 = self.graph.create_node('Output')
        output1.set_input(0, sum_)

        noop = self.graph.create_node('NoOp')
        noop.set_input(0, sum_)

        plus4 = self.graph.create_node('Plus', 20)
        plus4.set_input(0, noop)

        output2 = self.graph.create_node('Output')
        output2.set_input(0, plus4)

        # Check that the graph has the right output
        self.assertEqual({'Output2': 50}, self.graph.execute(output2))

        # Output graph to string
        string = self.graph.to_string()

        # Clear the graph
        orig_nodes = self.graph.nodes
        self.graph.clear()
        self.assertFalse(self.graph.nodes)

        print(string)

        # Read graph in from string
        self.graph.from_string(string)

        print('=' * 80)
        print(self.graph.to_string())

        # Verify that graph still produces same output
        output2 = self.graph.to_node('Output2')
        print(output2)
        self.assertEqual({'Output2': 50}, self.graph.execute(output2))

        # Verify that the graph nodes are still the same
        self.assertSetEqual(set(orig_nodes), set(self.graph.nodes))

        # Verify node connections remain intact
        for orig_node in orig_nodes:
            node = self.graph.to_node(orig_node.name)
            self.assertSetEqual(set(orig_node.inputs), set(node.inputs))
            self.assertSetEqual(set(orig_node.dependents), set(node.dependents))
