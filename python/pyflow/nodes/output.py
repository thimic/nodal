#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyflow.core.nodes import BaseNode


class Output(BaseNode):
    def __init__(self):
        super(Output, self).__init__()

    def _execute(self):
        if not self.has_input(0):
            return

        self._result = self.input(0).result
        print(self._result)
