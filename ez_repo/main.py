#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Main entry. Setup the command line interface then run the main function."""

from logging import INFO, DEBUG
from sys import argv

import argparse
import botocore.exceptions

from __init__ import __version__

import command
import error
import logger


def build_cli_interface():
    """
    Building command line interface and registering callback on (sub)commands
    available which will be executed in the main.
    :return: complete parser
    """
    parser = argparse.ArgumentParser(
        description="""Commandline client to send/get/search artefacts"""
        """ as in a Maven repository using a custom storage"""
        """(for now S3 only).""")

    parser.add_argument(
        '--version',
        action='store_true',
        help='Display version'
    )

    parser.add_argument(
        '-v',
        action='store_true',
        help='Augment verbosity'
    )

    parser.add_argument(
        '-vv',
        action='store_true',
        help='Augment greatly verbosity'
    )

    parser.add_argument(
        '-quiet',
        action='store_true',
        help='Activate silent mode'
    )

    subparsers = parser.add_subparsers()
    for cmd in command.COMMANDS:
        new_parser = subparsers.add_parser(name=cmd["name"], help=cmd["help"])
        new_parser.set_defaults(func=cmd["func"])
        for option in cmd["options"]:
            new_parser.add_argument(*option["args"], **option["kwargs"])

    return parser


def run(raw_args):
    """
    Parse arguments in parameter. Then call the function registered in the
    argument parser which matches them.
    :param raw_args:
    :return:
    """
    if "--version" in raw_args:
        print("version: ", __version__)
        return error.ReturnCode.success.value

    parser = build_cli_interface()
    args = parser.parse_args()

    if args.v:
        logger.set_global_level(INFO)

    if args.vv:
        logger.set_global_level(DEBUG)

    if args.quiet:
        logger.disable_logs()

    if "func" in args:
        try:
            args.func(args)
        except error.ConfigError as e:
            logger.LOGGER.error(e)
            return error.ReturnCode.config_error.value
        except error.ArtefactError as e:
            logger.LOGGER.error(e)
            return error.ReturnCode.artefact_error.value
        except error.ExpressionError as e:
            logger.LOGGER.error(e)
            return error.ReturnCode.expression_error.value
        except IOError as e:
            logger.LOGGER.error(e)
            return error.ReturnCode.artefact_error.value
        except botocore.exceptions.ClientError as e:
            logger.LOGGER.error("S3 error: %s" % e)
            return error.ReturnCode.s3_error.value
        except KeyboardInterrupt:
            logger.LOGGER.info("Interrupted")

    return error.ReturnCode.success.value


def main():
    """
    Main function. Entry point.
    :return:
    """
    return run(argv)


# Useful for dev testing (without installation)
if __name__ == "__main__":
    main()
