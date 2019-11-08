#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase

import nodal
from nodal.core import (
    CyclicDependencyException,
    NodeTypeMismatchException,
    MaxInputsExceededException
)


class TestVerifyConnection(TestCase):

    def test_simple_connection(self):
        node1 = nodal.nodes.NoOp()
        node2 = nodal.nodes.NoOp()
        self.assertTrue(node2.set_input(0, node1))

    def test_cyclic_dependency(self):
        node1 = nodal.nodes.NoOp()
        node2 = nodal.nodes.NoOp()
        node2.set_input(0, node1)
        self.assertRaises(CyclicDependencyException, node1.set_input, 0, node2)

    def test_self_dependency(self):
        node1 = nodal.nodes.NoOp()
        self.assertRaises(CyclicDependencyException, node1.set_input, 0, node1)

    def test_type_mismatch(self):

        # Check nodes of different types
        node1 = nodal.nodes.Plus()
        node2 = nodal.nodes.Text()
        self.assertRaises(NodeTypeMismatchException, node2.set_input, 0, node1)

        # Check nodes of same types
        node3 = nodal.nodes.Plus()
        self.assertTrue(node3.set_input(0, node1))

        # Check no ops connected to node with an op
        node4 = nodal.nodes.NoOp()
        self.assertTrue(node4.set_input(0, node3))

        # Check node with an op connected to no op
        node5 = nodal.nodes.Plus()
        self.assertTrue(node5.set_input(0, node4))

        # Check that no ops takes on the output type of its input
        self.assertEqual(node4.output_type, float)
        node6 = nodal.nodes.Text()
        self.assertRaises(NodeTypeMismatchException, node6.set_input, 0, node4)

    def test_input_overload(self):
        node1 = nodal.nodes.NoOp()
        node2 = nodal.nodes.NoOp()
        self.assertRaises(MaxInputsExceededException, node2.set_input, 1, node1)
