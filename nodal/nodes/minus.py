#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nodal.core.nodes import BaseNode


class Minus(BaseNode):

    _input_types = {
        -1: {'name': 'value', 'types': [int, float], 'default': 0.0}
    }
    _output_type = {'default': 0.0, 'type': float}
    _max_inputs = -1

    def _execute(self):
        if not self.inputs:
            self._result = self.value
            return
        inputs = sorted(
            [(k, v) for k, v in self.inputs.items()], key=lambda x: x[0]
        )
        self._result = inputs.pop(0)[1].result
        for input_idx, input_node in inputs:
            if input_node:
                self._result -= input_node.result
        self._result -= self.value

