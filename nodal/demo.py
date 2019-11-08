#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nodal

from nodal.graph import Graph


def demo():

    # Create a graph
    graph = Graph()

    # Create a Plus node with value 3
    plus1 = nodal.nodes.Plus(3)

    # Create a Plus node with value 7 and plug into the first Plus
    plus2 = graph.create_node('Plus')
    plus2.value = 7
    plus2.set_input(0, plus1)

    # Create an Output node and plug into the second Plus
    output = nodal.nodes.Output()
    output.set_input(0, plus2)
    print(output.name)

    # Execute graph
    graph.execute(output)


if __name__ == '__main__':
    demo()
