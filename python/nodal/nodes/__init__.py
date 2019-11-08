#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__node_classes__ = {}


def __load__():
    import glob
    import inspect
    import os

    from importlib import util as import_util

    from nodal.core.nodes.base import BaseNode

    this_file = inspect.getfile(inspect.currentframe())
    this_dir = os.path.dirname(this_file)
    for path in glob.glob(os.path.join(this_dir, '*.py')):
        if path == this_file:
            continue
        basename = os.path.basename(path)
        modulename = f'nodal.nodes.{os.path.splitext(basename)[0]}'
        spec = import_util.spec_from_file_location(modulename, path)
        module = import_util.module_from_spec(spec)
        spec.loader.exec_module(module)
        classes = inspect.getmembers(module, inspect.isclass)
        for name, class_ in classes:
            if class_ is BaseNode:
                continue
            if issubclass(class_, BaseNode):
                __node_classes__[class_.__name__] = class_


def __getattr__(name):
    if not __node_classes__:
        __load__()
    if name in __node_classes__:
        return __node_classes__[name]
    from nodal.core import NodeClassNotFoundException
    raise NodeClassNotFoundException(f'Unable to find node of class {name!r}.')
