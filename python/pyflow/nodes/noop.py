#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyflow.core.nodes import BaseNode


class NoOp(BaseNode):

    def _execute(self):
        if not self.has_input(0):
            return self._result
        self._result = self.input(0).result
