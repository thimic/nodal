#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import weakref
import yaml

from abc import ABCMeta, abstractmethod

from nodal import graph_utils, nodes
from nodal.core import Callbacks


class BaseNode(metaclass=ABCMeta):

    _input_types = {
        0: {'name': '_', 'types': [object], 'default': None}
    }
    _output_type = {'default': NotImplemented, 'type': object}
    _max_inputs = 1

    def __new__(cls, *args, **kwargs):
        inst = super().__new__(cls)
        inst._attrs = {'name': cls.__name__}
        inst._inputs = {}
        inst._outputs = []
        inst._result = NotImplemented
        inst._dirty = True
        return inst

    def __init__(self, *args, **kwargs):

        input_names = [k['name'] for k in self._input_types.values()]
        for input_ in self._input_types.values():
            self._attrs[input_['name']] = input_['default']

        input_len = len([
            i for i in self._input_types.values() if i['name'] != '_'
        ])
        if len(args) > input_len and -1 not in self._input_types:
            raise TypeError(
                f'{self.class_}.__init__() takes a maximum of {input_len} '
                f'positional argument{"s" if input_len != 1 else ""} but '
                f'{len(args)} {"were" if len(args) > 1 else "was"} given'
            )
        for idx, arg in enumerate(args):
            input_type = list(self._input_types.values())[idx]
            types = tuple(input_type['types'])
            if not isinstance(arg, types):
                raise TypeError(
                    f'Positional argument {idx} must be of type '
                    f'{", ".join([repr(t.__name__) for t in types])}, while '
                    f'{arg!r} is {type(arg).__name__!r}'
                )
            self._attrs[input_type['name']] = arg

        for key, value in kwargs.items():
            if key in self._attrs or key in input_names:
                if key != 'name' and key in self._attrs:
                    input_type = [
                        v for v in self._input_types.values()
                        if v['name'] == key
                    ][0]
                    types = tuple(input_type['types'])
                    if not isinstance(value, types):
                        raise TypeError(
                            f'Keyword argument {key!r} must be of type '
                            f'{", ".join([repr(t.__name__) for t in types])}, '
                            f'not {type(value).__name__!r}'
                        )
                self._attrs[key] = value
            else:
                raise TypeError(f'{self.class_}() takes no keyword {key!r}')

        self._result = self._output_type['default']

        Callbacks.trigger_on_create(self)

    def __getattr__(self, item):
        if item in self._attrs:
            return self._attrs[item]

    def __setattr__(self, key, value):
        attrs = self.__dict__.get('_attrs')
        if attrs and key in attrs:
            if attrs[key] == value:
                return
            attrs[key] = value
            self.__dict__['_dirty'] = True
            return
        super().__setattr__(key, value)

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

    def __hash__(self):
        return hash(tuple(self.attrs.keys()))

    def to_string(self):
        """
        Serialise node to string.

        Returns:
            str: Node as string

        """
        defaults = {v['name']: v['default'] for v in self._input_types.values()}
        data = {
            self.class_: {
                k: v for k, v in self.attrs.items()
                if k != '_' and defaults.get(k) != v
            }
        }
        string = yaml.dump(data, default_flow_style=True).strip()[1:-1]
        return string

    @classmethod
    def from_string(cls, string):
        """
        Create node from serialised string.

        Args:
            string (str): Node as string

        Returns:
            BaseNode: Created node

        """
        data = yaml.safe_load(f'{{{string}}}')
        key, value = list(data.items())[0]
        node = getattr(nodes, key)(**value)
        return node

    def delete(self):
        Callbacks.trigger_on_destroy(self)
        del self

    @property
    def class_(self):
        return self.__class__.__name__

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
