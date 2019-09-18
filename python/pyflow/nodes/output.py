#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyflow.nodes.noop import NoOp


class Output(NoOp):
    def __init__(self):
        super(Output, self).__init__()

    def _execute(self):
        super(Output, self)._execute()
        print(self._result)
