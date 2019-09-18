#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyflow.core.nodes import BaseNode


class Plus(BaseNode):

    _input_types = {
        -1: [int, float]
    }
    _output_type = float
    _max_inputs = -1

    def __init__(self, value=0):
        super(Plus, self).__init__()
        _attrs = {'name': None, 'value': value}
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
        if self.has_input(0):
            self._result = self.value + self.input(0).result
        else:
            self._result = self.value
