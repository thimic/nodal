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
    def _get_callback_dict(cls, callback):
        callback_dict = cls._callbacks.get(callback)
        if callback_dict is None:
            raise AttributeError(f'{callback!r} is not a supported callback.')
        return callback_dict

    @classmethod
    def _add_callback(cls, callback, func, node_classes=None):
        callback_dict = cls._get_callback_dict(callback)
        if isinstance(node_classes, str):
            node_classes = [node_classes]
        if not node_classes:
            callback_dict[None].append(func)
            return
        for node_class in node_classes:
            callback_dict[node_class].append(func)

    @classmethod
    def _remove_callback(cls, callback, func, node_classes=None):
        if isinstance(node_classes, str):
            node_classes = [node_classes]
        callback_dict = cls._get_callback_dict(callback)
        if not node_classes:
            if func in callback_dict[None]:
                callback_dict[None].remove(func)
            return
        for node_class in node_classes:
            if func in callback_dict[node_class]:
                callback_dict[node_class].remove(func)

    @classmethod
    def add_on_create(cls, func, node_classes=None):
        cls._add_callback('on_create', func, node_classes)

    @classmethod
    def remove_on_create(cls, func, node_classes=None):
        cls._remove_callback('on_create', func, node_classes)

    @classmethod
    def add_on_destroy(cls, func, node_classes=None):
        cls._add_callback('on_destroy', func, node_classes)

    @classmethod
    def remove_on_destroy(cls, func, node_classes=None):
        cls._remove_callback('on_destroy', func, node_classes)

    @classmethod
    def _trigger(cls, callback, node):
        callback_dict = cls._get_callback_dict(callback)
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

