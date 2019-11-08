#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nodal.core.nodes import BaseNode


class Text(BaseNode):

    _input_types = {
        0: [str]
    }
    _output_type = str

    def __init__(self, text=''):
        super(Text, self).__init__()
        self._attrs['text'] = text
        self._result = ''

    def _execute(self):
        if not self.input(0):
            self._result = self.text
        else:
            self._result = ' '.join([self.input(0).result, self.text])

    @property
    def text(self):
        return self._attrs['text']

    @text.setter
    def text(self, value):
        if value == self._attrs['text']:
            return
        self._dirty = True
        self._attrs['text'] = value
