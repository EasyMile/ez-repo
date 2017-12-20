#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class ReturnCode(Enum):
    """
    Enum class used to store the potential return code
    """
    success = 0
    config_error = 1
    s3_error = 2
    artefact_error = 3
    expression_error = 4
    not_implemented = 10


class ArtefactError(BaseException):
    pass


class ConfigError(BaseException):
    pass


class ExpressionError(BaseException):
    pass
