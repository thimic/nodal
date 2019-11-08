#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nodal.core.nodes import BaseNode


class NoOp(BaseNode):

    @property
    def output_type(self):
        if not self.has_input(0):
            return self._output_type
        return self.input(0).output_type

    def _execute(self):
        if not self.has_input(0):
            return self._result
        self._result = self.input(0).result
