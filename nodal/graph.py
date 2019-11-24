#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import nodal

from collections import Counter
from nodal.core import Callbacks, serialisation
from nodal.core.exceptions import CyclicDependencyException
from nodal.core.nodes import BaseNode
from typing import Dict, List, Union


class Graph:

    _name_pattern = re.compile(r'(?P<name>[a-zA-Z]+\w*)(?P<number>\d+)$')

    def __init__(self):
        self._nodes = []
        Callbacks.add_on_create(self._on_node_create)
        Callbacks.add_on_destroy(self._on_node_destroy)

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

    def to_string(self):
        lines = []
        sorted_nodes = self.sort()
        for idx, node in enumerate(sorted_nodes):
            lines.append(node.to_string())
            setter = False
            for child in node.dependents:
                if child != sorted_nodes[idx + 1]:
                    setter = True
            if setter:
                lines.append(f'set {id(node):x}')
            for input_idx, input_node in node.inputs.items():
                if input_node != sorted_nodes[idx - 1]:
                    lines.append(f'push {input_idx} ${id(input_node):x}')
        return '\n'.join(lines)

    @classmethod
    def from_string(cls, string: str) -> List[BaseNode]:
        nodes = []
        sets = {}
        node = None
        node_inputs = None
        push_buffer = {}
        lines = string.splitlines()
        for line_no, line in enumerate(lines, start=1):

            if line_no == len(lines):
                print('Last line!')

            # Check for and store set commands
            if line.startswith('set') and node:
                sets[line.replace('set ', '').strip()] = node
                if line_no != len(lines):
                    continue

            # Check for and store push commands
            elif line.startswith('push'):
                _, input_idx, node_id = line.strip().split(' ')
                input_idx = int(input_idx)
                node_id = node_id.strip('$')
                push_buffer[input_idx] = node_id
                if line_no != len(lines):
                    continue

            # We have a new node. First connect up the old one by going through
            # the push buffer.
            if node:
                if node_inputs != 0:
                    if push_buffer:
                        for idx, push in push_buffer.items():
                            node.set_input(idx, sets[push])
                        if node_inputs > len(push_buffer):
                            for i in range(node_inputs):
                                if i not in push_buffer:
                                    node.set_input(i, nodes[-1])
                                    break
                        push_buffer.clear()
                    elif nodes:
                        node.set_input(0, nodes[-1])

                nodes.append(node)

            if line_no == len(lines):
                return nodes

            # Create node
            node = BaseNode.from_string(line)
            node_inputs = BaseNode.inputs_from_string(line)

        return nodes
