#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import inspect
import os

import nodal

from nodal.core import NodeClassNotFoundException
from nodal.core.nodes import BaseNode

from unittest import TestCase


class TestNodes(TestCase):

    def test_nodes_getattr(self):

        noop = nodal.nodes.NoOp()
        self.assertTrue(noop)
        self.assertRaises(
            NodeClassNotFoundException,
            getattr, nodal.nodes, 'Foo'
        )

    def test_is_plugin(self):
        noop = nodal.nodes.NoOp()
        self.assertFalse(noop.is_plugin)

    def test_register_node(self):

        # Dummy node plugin
        class PluginNode(BaseNode):
            def _execute(self):
                return

        # Register dummy node
        nodal.nodes.register_node(PluginNode)

        # Create dummy node and verify its properties
        plugin = nodal.nodes.PluginNode()
        self.assertTrue(plugin.is_plugin)
        self.assertEqual('PluginNode1', plugin.name)

    def test_reload(self):

        # Check that NodalpathNode is not available as a plugin
        self.assertRaises(
            NodeClassNotFoundException,
            getattr, nodal.nodes, 'NodalpathNode'
        )

        # Set NODALPATH to a location where NodalpathNode can be found
        this_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
        test_root = os.path.dirname(os.path.dirname(this_dir))
        node1_path = os.path.join(test_root, 'resources', 'node1')
        node2_path = os.path.join(test_root, 'resources', 'node2')
        os.environ['NODALPATH'] = os.pathsep.join((node1_path, node2_path))

        # Reload nodes
        nodal.nodes.reload()

        # Verify that we have loaded NodalpathNode
        node1 = nodal.nodes.NodalpathNode1()
        self.assertTrue(node1)
        self.assertTrue(node1.is_plugin)
        node2 = nodal.nodes.NodalpathNode2()
        self.assertTrue(node2)
        self.assertTrue(node2.is_plugin)


