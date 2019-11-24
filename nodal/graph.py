#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import nodal

from collections import Counter
from nodal.core import Callbacks
from nodal.core.exceptions import CyclicDependencyException
from nodal.core.nodes import BaseNode
from typing import Dict, List, Union


class Graph:

    _name_pattern = re.compile(r'(?P<name>[a-zA-Z]+\w*)(?P<number>\d+)$')

    def __init__(self):
        self._nodes = []

    def __enter__(self):
        Callbacks.add_on_create(self._on_node_create)
        Callbacks.add_on_destroy(self._on_node_destroy)

    def __exit__(self, exc_type, exc_val, exc_tb):
        Callbacks.remove_on_create(self._on_node_create)
        Callbacks.remove_on_destroy(self._on_node_destroy)

    def __del__(self):
        Callbacks.remove_on_create(self._on_node_create)
        Callbacks.remove_on_destroy(self._on_node_destroy)

    @staticmethod
    def create_node(class_name: str, *args, **kwargs) -> BaseNode:
        return getattr(nodal.nodes, class_name)(*args, **kwargs)

    @staticmethod
    def delete_node(node: BaseNode):
        node.delete()

    @property
    def nodes(self) -> List[BaseNode]:
        return self._nodes

    def clear(self):
        self._nodes.clear()

    def execute(self, nodes: Union[BaseNode, List[BaseNode]]) -> Dict[str, object]:
        if isinstance(nodes, BaseNode):
            nodes = [nodes]
        results = {}
        for node in nodes:
            results[node.name] = node.execute()
        return results

    def _on_node_create(self, node: BaseNode):
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

    def _on_node_destroy(self, node: BaseNode):
        if node not in self._nodes:
            return
        self._nodes.remove(node)

    def to_node(self, name: str) -> Union[BaseNode, None]:
        nodes = [n for n in self.nodes if n.name == name]
        if not nodes:
            return
        return nodes[0]

    def top_nodes(self) -> list:
        return [n for n in self.nodes if not n.inputs]

    def sort(self) -> list:
        """
        Topical sort of DAG using Kahn's algorithm.

        Returns:
            list: Sorted list of nodes

        """
        inputs = Counter()
        top_nodes = self.top_nodes()
        sorted_nodes = []
        while top_nodes:
            node = top_nodes.pop(0)
            sorted_nodes.append(node)
            for child in node.dependents:
                if child.name not in inputs:
                    inputs[child.name] = len(child.inputs)
                inputs[child.name] -= 1
                if not inputs[child.name]:
                    inputs.pop(child.name)
                    top_nodes.insert(0, child)
        if inputs:
            raise CyclicDependencyException('Graph is cyclical!')
        return sorted_nodes
