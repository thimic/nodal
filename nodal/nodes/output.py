#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nodal.nodes.noop import NoOp


class Output(NoOp):

    def _execute(self):
        super(Output, self)._execute()
        print(' RESULT '.center(80, '='))
        print(f'{self.name}: {self._result}')
        print('=' * 80)
