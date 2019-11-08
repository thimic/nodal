#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class PyFlowException(BaseException):

    pass


class NodeConnectionException(PyFlowException):

    pass


class CyclicDependencyException(NodeConnectionException):

    pass


class NodeTypeMismatchException(NodeConnectionException):

    pass


class MaxInputsExceededException(NodeConnectionException):

    pass


class NodeClassNotFoundException(PyFlowException):

    pass
