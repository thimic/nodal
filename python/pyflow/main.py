#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyflow


def main():

    num1 = pyflow.nodes.Plus(5)

    num2 = pyflow.nodes.Plus(7)
    num2.set_input(0, num1)

    noop = pyflow.nodes.NoOp()
    noop.set_input(0, num2)

    num3 = pyflow.nodes.Plus(-2)
    num3.set_input(0, noop)

    num4 = pyflow.nodes.Plus(13)
    num4.set_input(0, num3)

    output = pyflow.nodes.Output()
    output.set_input(0, num4)

    output.execute()

    num1.value = 23

    output.execute()

    num3.set_input(0, None)

    output.execute()


if __name__ == '__main__':
    main()
