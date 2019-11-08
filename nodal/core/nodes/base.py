#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import weakref

from abc import ABCMeta, abstractmethod

from nodal.core import Callbacks
from nodal import graph_utils


class BaseNode(metaclass=ABCMeta):

    _input_types = {
        0: [object]
    }
    _output_type = object
    _max_inputs = 1

    def __init__(self):
        self._inputs = {}
        self._outputs = []
        self._result = []
        self._dirty = True

        self._attrs = {'name': self.class_}

        Callbacks.trigger_on_create(self)

    def __del__(self):
        """
        Class destructor. Called when the node is garbage collected. Time of
        garbage collection cannot be predicted with certainty, so this method is
        only implemented as a last resort. Use self.delete() for node deletion.
        """
        Callbacks.trigger_on_destroy(self)

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

    def delete(self):
        Callbacks.trigger_on_destroy(self)
        del self

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
    def input_types(self):
        return self._input_types

    @property
    def output_type(self):
        return self._output_type

    @property
    def max_inputs(self):
        return self._max_inputs

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
        # De-referencing weakref
        if self.max_inputs == -1:
            return {k: v() for k, v in self._inputs.items()}
        else:
            return {i: self.input(i) for i in range(self.max_inputs)}

    @property
    def dependents(self):
        # De-referencing weakref
        return [o() for o in self._outputs]

    def input(self, index):
        graph_utils.verify_input_index(self, index)
        if not self._inputs.get(index):
            return None

        # De-referencing weakref
        return self._inputs[index]()

    def set_input(self, index, node):
        # Verify connection
        graph_utils.verify_connection(self, index, node)

        # About to change node connections. Node is dirty!
        self._dirty = True

        # Unplug if node is None
        if node is None:
            if self._inputs.get(index):
                weak_node = self._inputs.pop(index)
                node = weak_node()
                if weak_node in node._outputs:
                    node._outputs.remove(weak_node)
            return True

        # Plug set input to node
        self._inputs[index] = weakref.ref(node)
        node._outputs.append(weakref.ref(self))
        return True

    def has_input(self, index):
        return bool(self._inputs.get(index))

    @abstractmethod
    def _execute(self):
        pass

    def execute(self):
        self._execute()
        self._dirty = False
        return self._result
