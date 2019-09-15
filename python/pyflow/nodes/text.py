#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyflow.core.nodes import BaseNode


class Text(BaseNode):

    def __init__(self, text=''):
        super(Text, self).__init__()
        self._attrs = {'name': None, 'text': text}

    def _execute(self):
        self._result.append(self.text)

    @property
    def text(self):
        return self._attrs['text']

    @text.setter
    def text(self, value):
        self._dirty = True
        self._attrs['text'] = value
