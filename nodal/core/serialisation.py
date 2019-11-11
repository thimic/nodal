#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict


def analyse(top_nodes, parent_node=None, items=None):
    pushes = set()
    inputs = defaultdict(list)
    items = items or []
    for top_node in top_nodes:
        inputs[top_node].append(parent_node)
        if top_node.dependents and len(top_node.dependents[0].inputs) > 1:
            pushes.add(top_node)
        items.append(top_node)
        node = top_node
        while node.dependents:
            if len(node.dependents) > 1:
                branch_items, branch_pushes, branch_inputs = analyse(node.dependents[1:], node, items)
                for branch_item in branch_items:
                    if branch_item in items:
                        continue
                    items.append(branch_item)
                    if branch_item in branch_pushes:
                        pushes.add(branch_item)
                    if branch_item in branch_inputs:
                        inputs[branch_item] += branch_inputs
                pushes.add(node)
                inputs[node.dependents[0]].append(node)
            node = node.dependents[0]
            if node in items:
                break
            if len(node.inputs) > 1:
                for idx, input_node in node.inputs.items():
                    inputs[node].append(input_node)
            items.append(node)
    return items, pushes, inputs


def to_string(top_nodes):
    items = []
    nodes, pushes, inputs = analyse(top_nodes)
    for node in nodes:
        node_inputs = inputs.get(node) or []
        for node_input in node_inputs:
            if node_input is None:
                items.append('set_input 0')
            else:
                items.append(f'set_input {id(node_input):x}')
        if node in pushes:
            items.append(f'push {id(node):x}')
        items.append(node.to_string())
    return '\n'.join(items)
