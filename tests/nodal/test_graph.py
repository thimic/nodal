#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase

import nodal

from nodal import Graph
from nodal.core.callbacks import Callbacks


class TestGraph(TestCase):

    def assertConnectionsEqual(self, node1, node2):
        inputs1 = [n for n in node1.inputs.values()]
        inputs2 = [n for n in node2.inputs.values()]
        self.assertListEqual(inputs1, inputs2)

        dependents1 = [n for n in node1.dependents]
        dependents2 = [n for n in node2.dependents]
        self.assertSetEqual(set(dependents1), set(dependents2))

    def setUp(self):
        self.graph = Graph()

    def tearDown(self):
        for node in self.graph.nodes:
            node.delete()
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

    def test_sort(self):

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

        # Confirm sort order is correct
        self.assertListEqual(
            [plus1, plus2, plus3, sum_, noop, plus4, output2, output1],
            self.graph.sort()
        )

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

        minus1 = self.graph.create_node('Minus', 5)
        minus1.set_input(0, sum_)

        output1 = self.graph.create_node('Output')
        output1.set_input(0, minus1)
        self.assertEqual({'Output1': 25}, self.graph.execute(output1))

        noop = self.graph.create_node('NoOp')
        noop.set_input(0, minus1)

        plus4 = self.graph.create_node('Plus', 20)  # 45
        plus4.set_input(0, noop)
        self.assertEqual(45, plus4.result)

        plus5 = self.graph.create_node('Plus', 50)  # 55
        plus5.set_input(0, plus1)
        self.assertEqual(55, plus5.result)

        minus2 = self.graph.create_node('Minus', 30)  # -25
        minus2.set_input(0, plus1)
        self.assertEqual(-25, minus2.result)

        minus3 = self.graph.create_node('Minus', 5)  # 10
        minus3.set_input(0, plus4)
        minus3.set_input(1, plus5)
        minus3.set_input(2, minus2)
        self.assertEqual(10, minus3.result)

        output2 = self.graph.create_node('Output')
        output2.set_input(0, minus3)

        # Check that the graph has the right output
        self.assertEqual({'Output2': 10}, self.graph.execute(output2))

        # Output graph to string
        string = self.graph.to_string()
        print(string)

        # Copy original nodes to a new list for later comparison
        orig_nodes_sorted = self.graph.sort()[:]

        # Clear the graph
        self.graph.clear()
        self.assertFalse(self.graph.nodes)

        # Read graph in from string
        parsed_nodes = self.graph.from_string(string)

        print('=' * 80)
        print(self.graph.to_string())

        # Verify that graph still produces same output
        output1 = self.graph.to_node('Output1')
        self.assertEqual({'Output1': 25}, self.graph.execute(output1))
        output2 = self.graph.to_node('Output2')
        self.assertEqual({'Output2': 10}, self.graph.execute(output2))

        # self.assertListEqual(parsed_nodes, self.graph.nodes)
        # self.assertListEqual(orig_nodes_sorted, self.graph.nodes)
        # for orig_node, parsed_node in zip(orig_nodes_sorted, self.graph.nodes):
        #     self.assertConnectionsEqual(orig_node, parsed_node)

