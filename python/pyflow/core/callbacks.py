#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict


class Callbacks:

    _on_create = defaultdict(list)

    @classmethod
    def clear(cls):
        cls._on_create = defaultdict(list)

    @classmethod
    def add_on_create(cls, func, node_classes=None):
        if not node_classes:
            cls._on_create[None].append(func)
            return
        for node_class in node_classes:
            cls._on_create[node_class].append(func)

    @classmethod
    def trigger_on_create(cls, node):
        for node_class, callbacks in cls._on_create.items():
            if node_class is None:
                for callback in callbacks:
                    callback(node)
            else:
                if node.class_ != node_class:
                    continue
                for callback in callbacks:
                    callback(node)

