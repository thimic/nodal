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
    def create_node(class_name, *args, **kwargs):
        return getattr(nodal.nodes, class_name)(*args, **kwargs)

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

    def to_node(self, name):
        nodes = [n for n in self.nodes if n.name == name]
        if not nodes:
            return
        return nodes[0]

    def top_nodes(self):
        return [n for n in self.nodes if not n.inputs]

    def to_string(self):
        items = []
        for top_node in self.top_nodes():
            items.append('set_input 0')
            if top_node.dependents and len(top_node.dependents[0].inputs) > 1:
                items.append(f'push {id(top_node):x}')
            items.append(top_node)
            node = top_node
            while node.dependents:
                node = node.dependents[0]
                if node in items:
                    continue
                if len(node.inputs) > 1:
                    for idx, input_node in node.inputs.items():
                        items.append(f'set_input {id(input_node):x}')
                items.append(node)
        items = [i.to_string() if isinstance(i, BaseNode) else i for i in items]
        return '\n'.join(items)

    @classmethod
    def from_string(cls, string):
        push = {}
        set_inputs = {}
        push_buffer = ''
        input_buffer = []
        nodes = []
        for line in string.splitlines():
            if line.startswith('push'):
                push_buffer = line.replace('push ', '').strip()
                continue
            elif line.startswith('set_input'):
                input_buffer.append(line.replace('set_input ', '').strip())
                continue
            node = BaseNode.from_string(line)
            if not input_buffer and nodes:
                node.set_input(0, nodes[-1])
            if push_buffer:
                push[push_buffer] = node
            if input_buffer:
                set_inputs[node] = input_buffer
            push_buffer = ''
            input_buffer = []
            nodes.append(node)
        for node, inputs in set_inputs.items():
            for idx, input_id in enumerate(inputs):
                if input_id == '0':
                    input_node = None
                else:
                    input_node = push[input_id]
                node.set_input(idx, input_node)
