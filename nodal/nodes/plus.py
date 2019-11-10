#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nodal.core.nodes import BaseNode


class Plus(BaseNode):

    _input_types = {
        -1: {'name': 'value', 'types': [int, float], 'default': 0.0}
    }
    _output_type = {'default': 0.0, 'type': float}
    _max_inputs = -1

    def _execute(self):
        self._result = self.value
        for index, input_node in self.inputs.items():
            if input_node:
                self._result += input_node.result

