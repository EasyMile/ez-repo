#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Config file reader"""

from os.path import isfile
from artefact import Artefact

try:
    import configparser as cp
except ImportError as e:
    import ConfigParser as cp

from logger import LOGGER


def load_config(path):
    if not isfile(path):
        raise IOError("Config file {} not reachable".format(path))

    config = cp.ConfigParser()
    config.read(path)

    LOGGER.debug("Loaded configuration file %s" % path)
    return [Artefact(**dict(config.items(section)))
            for section in config.sections()]
