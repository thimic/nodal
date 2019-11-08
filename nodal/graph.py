#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import nodal
from nodal.core import Callbacks
from nodal.core.nodes import BaseNode


class Graph:

    _name_pattern = re.compile(r'(?P<name>[a-zA-Z]+\w*)(?P<number>\d+)$')

    def __init__(self):
        self._nodes = []
        Callbacks.add_on_create(self._on_node_create)
        Callbacks.add_on_destroy(self._on_node_destroy)

    @staticmethod
    def create_node(class_name):
        return getattr(nodal.nodes, class_name)()

    @staticmethod
    def delete_node(node):
        node.delete()

    @property
    def nodes(self):
        return self._nodes

    def clear(self):
        self._nodes.clear()

    def execute(self, nodes):
        if isinstance(nodes, BaseNode):
            nodes = [nodes]
        results = {}
        for node in nodes:
            results[node.name] = node.execute()
        return results

    def _on_node_create(self, node):
        match = self._name_pattern.match(node.name)
        if not match:
            node.name = f'{node.name}1'
        existing_names = [n.name for n in self._nodes]
        while node.name in existing_names:
            match = self._name_pattern.match(node.name)
            name = match.groupdict().get('name') or node.name
            number = int(match.groupdict().get('number', '0'))
            node.name = f'{name}{number + 1}'
        self._nodes.append(node)

    def _on_node_destroy(self, node):
        if node not in self._nodes:
            return
        self._nodes.remove(node)
