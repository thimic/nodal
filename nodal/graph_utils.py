#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nodal.core.exceptions import (
    CyclicDependencyException,
    MaxInputsExceededException,
    NodeTypeMismatchException
)


def verify_dependencies(node, input_node):
    """
    Checks for cyclic dependencies.

    Args:
        node (BaseNode): Current node
        input_node (BaseNode): Node to connect current node's input to

    Raises:
        CyclicDependencyException: When node's input chain ends up referring
                                   back to this node.

    """
    if input_node is node:
        msg = f'Unable to set {input_node} as input for {node}.'
        raise CyclicDependencyException(msg)
    for input_idx, upstream_node in input_node.inputs.items():
        if not upstream_node:
            continue
        if upstream_node is node:
            msg = f'Unable to set {upstream_node} as input for {node}.'
            raise CyclicDependencyException(msg)
        verify_dependencies(node, upstream_node)


def verify_type_match(node, input_idx, input_node):
    """
    Verifies that the input_node outputs a type supported by node's input index.

    Args:
        node (BaseNode): Current node
        input_idx (int): Current node's input to be connected to input_node
        input_node (BaseNode): Node to connect current node's input to

    Raises:
        NodeTypeMismatchException: When input_node does not output a type
                                   supported by node's input index.

    """
    if -1 in node.input_types:
        input_types = node.input_types[-1]
    else:
        input_types = node.input_types[input_idx]
    if not any(issubclass(input_node.output_type, t) for t in input_types):
        msg = (
            f'Input {input_idx} for node {node.name!r} expects type(s) '
            f'{", ".join([repr(t.__name__) for t in input_types])}, while node '
            f'{input_node.name!r} only outputs type '
            f'{input_node.output_type.__name__!r}.'
        )
        raise NodeTypeMismatchException(msg)


def verify_input_index(node, input_idx):
    """
    Verifies that input index does not exceed node's max inputs.

    Args:
        node (BaseNode): Current node
        input_idx (int): Current node's input to be connected to input_node

    Raises:
        MaxInputsExceededException: When input_idx exceeds node's max_inputs

    """
    # Verify Index
    if node.max_inputs is not -1 and input_idx + 1 > node.max_inputs:
        raise MaxInputsExceededException


def verify_connection(node, input_idx, input_node):
    """
    Performs various verification checks before allowing node and input_node to
    be connected.

    Args:
        node (BaseNode): Current node
        input_idx (int): Current node's input to be connected to input_node
        input_node (BaseNode): Node to connect current node's input to

    Raises:
        CyclicDependencyException: When verification fails

    """
    if input_node is None:
        return
    verify_input_index(node, input_idx)
    verify_type_match(node, input_idx, input_node)
    verify_dependencies(node, input_node)
