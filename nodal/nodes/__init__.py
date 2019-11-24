#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from enum import Enum

from nodal.core.nodes.base import BaseNode

__node_classes__ = defaultdict(dict)


class Origin(Enum):
    """
    Enum used to identify a node as native or plugin.
    """
    Native = 0
    Plugin = 1


def __load__():
    """
    Loads native and plugin nodes by trawling and importing python scripts from
    internal nodal/nodes directory and external $NODALPATH entries. Stores
    discovered nodes in __node_classes__.
    """
    import glob
    import inspect
    import os

    from importlib import util as import_util

    this_file = inspect.getfile(inspect.currentframe())
    native_dir = os.path.dirname(this_file)
    plugin_dirs = [d for d in os.getenv('NODALPATH', '').split(os.pathsep) if d]
    node_paths = list(zip([Origin.Plugin] * len(plugin_dirs), plugin_dirs))
    node_paths.insert(0, (Origin.Native, native_dir))
    for origin, origin_path in node_paths:
        for path in glob.glob(os.path.join(origin_path, '*.py')):
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
                    class_._is_plugin = bool(origin.value)
                    __node_classes__[origin][class_.__name__] = class_


def reload():
    """
    Scan for new plugins that might have been added at runtime via $NODALPATH.
    """
    __load__()


def register_node(node_class: BaseNode):
    """
    Register a new node. Must be a subclass of BaseNode.

    Args:
        node_class (BaseNode): Node class to register

    """
    node_class._is_plugin = True
    __node_classes__[Origin.Plugin][node_class.__name__] = node_class


def __getattr__(name: str) -> BaseNode:
    """
    Looks up node with the given name in __node_classes__.
    Args:
        name (str): Node class name

    Returns:
        BaseNode: Registered node if found

    Raises:
        NodeClassNotFoundException: If node class by the given name is not found

    """
    if not __node_classes__[Origin.Native]:
        __load__()
    for origin in (Origin.Plugin, Origin.Native):
        if name in __node_classes__[origin]:
            return __node_classes__[origin][name]
    from nodal.core import NodeClassNotFoundException
    raise NodeClassNotFoundException(f'Unable to find node of class {name!r}.')
