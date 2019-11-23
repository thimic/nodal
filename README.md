# Nodal

https://github.com/thimic/nodal/workflows/lint_tests/badge.svg
[![Actions Status](https://github.com/thimic/nodal/workflows/lint_tests/badge.svg)](https://github.com/thimic/nodal/actions)


An execution graph for Python tasks.

## Example

```python
import nodal

from nodal.graph import Graph


def demo():

    # Create a graph
    graph = Graph()

    # Create a Plus node with value 3
    plus1 = nodal.nodes.Plus(3)

    # Create a Plus node with value 7 and plug into the first Plus
    plus2 = graph.create_node('Plus', 7)
    plus2.set_input(0, plus1)

    # Create an Output node and plug into the second Plus
    output = nodal.nodes.Output()
    output.set_input(0, plus2)

    # Execute graph
    graph.execute(output)


if __name__ == '__main__':
    demo()

```
