#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase

import pyflow
from pyflow.core.exceptions import CyclicDependencyException


class TestVerifyConnection(TestCase):

    def test_simple_connection(self):
        node1 = pyflow.nodes.NoOp()
        node2 = pyflow.nodes.NoOp()
        self.assertTrue(node2.set_input(0, node1))

    def test_cyclic_dependency(self):
        node1 = pyflow.nodes.NoOp()
        node2 = pyflow.nodes.NoOp()
        node2.set_input(0, node1)
        self.assertRaises(CyclicDependencyException, node1.set_input, 0, node2)

    def test_self_dependency(self):
        node1 = pyflow.nodes.NoOp()
        self.assertRaises(CyclicDependencyException, node1.set_input, 0, node1)
