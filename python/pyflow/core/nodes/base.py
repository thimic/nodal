#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from pyflow.core import Callbacks
from pyflow.core.exceptions import MaxInputsExceededException
from pyflow import graph_utils


class BaseNode(metaclass=ABCMeta):

    _input_types = {
        0: [type]
    }
    _output_type = type
    _max_inputs = 1

    def __init__(self):
        self._inputs = {}
        self._outputs = []
        self._result = []
        self._dirty = True

        self._attrs = {'name': self.class_}

        Callbacks.trigger_on_create(self)

    def __repr__(self):
        return f'<{self.class_}(name={self.name!r}) at 0x{id(self):x}>'

    def __eq__(self, other):
        type_match = type(self) == type(other)
        if not type_match:
            return False
        attr_match = all(
            [self.attrs[a] == other.attrs.get(a) for a in self.attrs]
        )
        return attr_match

    @property
    def class_(self):
        return self.__class__.__name__

    @property
    def name(self):
        return self._attrs['name']

    @name.setter
    def name(self, value):
        self._attrs['name'] = value

    @property
    def attrs(self):
        return self._attrs

    @property
    def dirty(self):
        input_dirty = False
        if self.has_input(0):
            input_dirty = self.input(0).dirty
        return self._dirty or input_dirty

    @property
    def result(self):
        if not self._result or self.dirty:
            self.execute()
        return self._result

    @property
    def inputs(self):
        return self._inputs

    @property
    def dependents(self):
        return self._outputs

    def input(self, index):
        return self._inputs[index]

    def set_input(self, index, node):
        # Verify Index
        if index + 1 > self._max_inputs:
            raise MaxInputsExceededException

        # About to change node connections. Node is dirty!
        self._dirty = True

        # Unplug if node is None
        if node is None:
            if self.inputs[index]:
                node = self.inputs.pop(index)
                node.dependents.remove(self)
            return True

        # Plug set input to node
        graph_utils.verify_connection(self, node)
        self._inputs[index] = node
        node.dependents.append(self)
        return True

    def has_input(self, index):
        return bool(self._inputs.get(index))

    @abstractmethod
    def _execute(self):
        pass

    def execute(self):
        self._execute()
        self._dirty = False
