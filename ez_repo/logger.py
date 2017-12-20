#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Logger encapsulation to enable colored logs."""

from logging import Logger, getLogger, StreamHandler, INFO, CRITICAL, disable

from colorlog import ColoredFormatter

formatter = ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)


def disable_logs():
    disable(CRITICAL)


def init_logger(logger):
    streamH = StreamHandler()
    streamH.setFormatter(formatter)
    logger.addHandler(streamH)


def set_global_level(level):
    LOGGER.setLevel(level)
    getLogger().setLevel(level)


LOGGER = Logger("artefact", INFO)
init_logger(LOGGER)
init_logger(getLogger())
