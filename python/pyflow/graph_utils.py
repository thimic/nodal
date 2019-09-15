#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyflow.core.exceptions import CyclicDependencyException


def verify_connection(node, input_node):
    while input_node.has_input(0) or input_node is node:
        if input_node is node:
            msg = f'Unable to set {input_node} as input for {node}.'
            raise CyclicDependencyException(msg)
        input_node = input_node.input(0)
