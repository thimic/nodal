#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict


class Callbacks:

    _callbacks = {
        'on_create': defaultdict(list),
        'on_destroy': defaultdict(list)
    }

    @classmethod
    def clear(cls):
        for k, v in cls._callbacks.items():
            v.clear()

    @classmethod
    def _add_callback(cls, callback, func, node_classes=None):
        callback_dict = cls._callbacks.get(callback)
        if callback_dict is None:
            raise AttributeError(f'{callback!r} is not a supported callback.')
        if not node_classes:
            callback_dict[None].append(func)
            return
        for node_class in node_classes:
            callback_dict[node_class].append(func)

    @classmethod
    def add_on_create(cls, func, node_classes=None):
        cls._add_callback('on_create', func, node_classes)

    @classmethod
    def add_on_destroy(cls, func, node_classes=None):
        cls._add_callback('on_destroy', func, node_classes)

    @classmethod
    def _trigger(cls, callback, node):
        callback_dict = cls._callbacks.get(callback)
        if callback_dict is None:
            raise AttributeError(f'{callback!r} is not a supported callback.')
        for node_class, callbacks in callback_dict.items():
            if node_class is None:
                for callback in callbacks:
                    callback(node)
            else:
                if node.class_ != node_class:
                    continue
                for callback in callbacks:
                    callback(node)

    @classmethod
    def trigger_on_create(cls, node):
        cls._trigger('on_create', node)

    @classmethod
    def trigger_on_destroy(cls, node):
        cls._trigger('on_destroy', node)

