#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nodal.core.nodes import BaseNode


class Text(BaseNode):

    _input_types = {
        0: {'name': 'text', 'types': [str], 'default': ''}
    }
    _output_type = {'default': '', 'type': str}

    def _execute(self):
        if not self.input(0):
            self._result = self.text
        else:
            self._result = ' '.join([self.input(0).result, self.text])
