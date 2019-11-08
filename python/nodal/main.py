#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nodal


def main():

    num1 = nodal.nodes.Plus(5)

    num2 = nodal.nodes.Plus(7)
    num2.set_input(0, num1)

    noop = nodal.nodes.NoOp()
    noop.set_input(0, num2)

    num3 = nodal.nodes.Plus(-2)
    num3.set_input(0, noop)

    num4 = nodal.nodes.Plus(13)
    num4.set_input(0, num3)

    output = nodal.nodes.Output()
    output.set_input(0, num4)

    output.execute()

    num1.value = 23

    output.execute()

    num3.set_input(0, None)

    output.execute()


if __name__ == '__main__':
    main()
