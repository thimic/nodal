#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nodal.core.nodes import BaseNode


class Plus(BaseNode):

    _input_types = {
        -1: [int, float]
    }
    _output_type = float
    _max_inputs = -1

    def __init__(self, value=0):
        super(Plus, self).__init__()
        self._attrs['value'] = value
        self._result = 0

    @property
    def value(self):
        return self._attrs['value']

    @value.setter
    def value(self, value):
        if value == self._attrs['value']:
            return
        self._attrs['value'] = value
        self._dirty = True

    def _execute(self):
        self._result = self.value
        for index, input_node in self.inputs.items():
            if input_node:
                self._result += input_node.result

