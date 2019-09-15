#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import pyflow
from pyflow.core import Callbacks


class Graph:

    _name_pattern = re.compile(r'(?P<name>[a-zA-Z]+\w*)(?P<number>\d+)$')

    def __init__(self):
        self._nodes = []
        Callbacks.add_on_create(self._on_node_create)

    @staticmethod
    def create_node(class_name):
        return getattr(pyflow.nodes, class_name)()

    @property
    def nodes(self):
        return self._nodes

    def execute(self, nodes):
        pass

    def _on_node_create(self, node):
        match = self._name_pattern.match(node.name)
        if not match:
            node.name = f'{node.name}1'
        existing_names = [n.name for n in self._nodes]
        while node.name in existing_names:
            match = self._name_pattern.match(node.name)
            if not match:
                name = node.name
                number = 0
            else:
                name = match.groupdict().get('name') or node.name
                number = int(match.groupdict().get('number', '0'))
            node.name = f'{name}{number + 1}'
        self._nodes.append(node)
