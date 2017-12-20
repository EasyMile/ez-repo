#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    input = raw_input
except NameError:
    pass

import ez_repo.s3 as s3
import ez_repo.artefact as artefact
from ez_repo.error import ArtefactError
from ez_repo.config import load_config
from ez_repo.logger import LOGGER


COMMANDS = []


def expression_argument():
    return [
        {
            "args": ["--expression"],
            "kwargs": {
                "required": True,
                "dest": "expression",
                "help": "search expression with which to match s3 objects"
            }
        }
    ]


def storage_arguments():
    return [
        {
            "args": ["--storage-endpoint"],
            "kwargs": {
                "dest": "storage_endpoint",
                "help": "The storage endpoint to interact with "
                "(bucket name for S3)",
                "required": True
            }
        },
        {
            "args": ["--storage-type"],
            "kwargs": {
                "dest": "storage_type",
                "help": "The storage type to use",
                "choices": ["s3"],
                "default": "s3"
            }
        }
    ]


def cli_cmd(name, help, options):
    def wrapper(func):
        def wrapped_func(args):
            func(args)

        COMMANDS.append({
            "func": func,
            "name": name,
            "help": help,
            "options": options
        })

        return wrapped_func
    return wrapper


@cli_cmd(name="upload",
         help="Upload artefact(s)",
         options=storage_arguments() + [
             {
                 "args": ["-i", "--interactive"],
                 "kwargs":{
                     "dest": "interactive",
                     "action": "store_true",
                     "help": "Prompt informations if not given via arguments"
                 }
             },
             {
                 "args": ["--repository"],
                 "kwargs": {
                     "dest": "repository",
                     "choices": artefact.REPOSITORIES,
                     "help": "Repository in which to upload the artefact"
                 }
             },
             {
                "args": ["--society"],
                "kwargs": {
                    "dest": "society",
                    "help": "Society owner of artefact (example:easymile)"
                }
             },
             {
                "args": ["--name"],
                "kwargs": {
                    "dest": "name",
                    "help":
                    "Artefact name, usually product name(example: toolbox)"
                }
             },
             {
                 "args": ["--artefactversion"],
                 "kwargs": {
                     "dest": "version",
                     "help": "Artefact version"
                 }
             },
             {
                 "args": ["--extension"],
                 "kwargs": {
                     "dest": "extension",
                     "help": "Artefact extension (example: .zip)"
                 }
             },
             {
                 "args": ["--classifiers"],
                 "kwargs": {
                     "dest": "classifiers",
                     "help": "Artefact classifiers (example: Linux-x86_64)"
                 }
             },
             {
                 "args": ["--metadata"],
                 "kwargs": {
                     "dest": "metadata",
                     "help": "AWS metadata to put on uploaded object."
                     "example: name:value;date:today;commit:aze2234aze"
                 },
             },
             {
                 "args": ["--file"],
                 "kwargs": {
                     "dest": "local_path",
                     "help": "Local file to upload"
                 }
             },
             {
                 "args": ["--config"],
                 "kwargs": {
                     "dest": "config",
                     "help": "Configuration file to read artefact infos from"
                     "(example:./upload.conf"
                 }
             },
             {
                 "args": ["--filter"],
                 "kwargs": {
                     "dest": "filter",
                     "default": "*",
                     "help": "Filter onto artefacts to upload"
                     "(example:mapeditor|rapidash-ez10"
                 }
             }])
def upload(args):
    """
    Upload artefacts interactively/programmatically, via reading a
    configuration file or directly via passing arguments.
    :return:
    """
    # Config mode and cli args mode non cumulable
    if args.config:
        artefacts = load_config(args.config)
    else:
        artefacts = [artefact.Artefact(**vars(args))]

    if not artefacts:
        LOGGER.warning("No artefact to upload")
        return

    storage = s3.S3Storage(args.storage_endpoint)
    custom_filter = _create_filter(args.filter)

    for item in artefacts:
        if args.interactive:
            _prompt_missing_infos(item)

        missing_infos = item.missing_infos()
        if len(missing_infos) >= 1:
            raise ArtefactError(
                "Missing informations on artefact {}:\n{}".format(
                    item.local_path, "\n".join(missing_infos)))

        if custom_filter(item.name):
            LOGGER.debug(
                "{} upload skipped!!!".format(item.get_path())
            )
            continue

        if item.repository not in artefact.REPOSITORIES:
            raise ArtefactError(
                "Repository %s not allowed. Available choices are \"%s\"" % (
                    item.repository, " ".join(artefact.REPOSITORIES)))

        storage.upload(item)

        LOGGER.info("Successfully uploaded the artefact {} "
                    "-> endpoint: {}, path: {}".format(
                        item.local_path,
                        storage.endpoint,
                        item.get_path()
                    ))


@cli_cmd(name="delete",
         help="Delete artefact(s)",
         options=storage_arguments() + expression_argument())
def delete(args):
    """
    Delete artefacts.
    """
    storage = s3.S3Storage(args.storage_endpoint)
    matching_objects = storage.search(args.expression)

    if not matching_objects:
        LOGGER.warning("Did not found any matching folders/artefacts")
        return

    LOGGER.info("{} artefacts to delete:\n{}".format(
        len(matching_objects),
        "\n".join(matching_objects)
    ))

    if _user_confirm():
        for name in matching_objects:
            storage.delete(name)
            LOGGER.info("{} deleted".format(name))
    else:
        LOGGER.info("Aborted")


@cli_cmd(name="download",
         help="Download artefact(s)",
         options=storage_arguments() + expression_argument())
def download(args):
    """
    Download artefacts matching the regular expressions.
    """
    storage = s3.S3Storage(args.storage_endpoint)
    matching_objects = storage.search(args.expression)

    if not matching_objects:
        LOGGER.warning("Did not found any matching folders/artefacts")
        return

    LOGGER.info("{} artefacts to download:\n{}".format(
        len(matching_objects),
        "\n".join(matching_objects)))

    if _user_confirm():
        for name in matching_objects:
            storage.download(name)
            LOGGER.info("{} downloaded in current directory".format(name))
    else:
        LOGGER.info("Aborted")


@cli_cmd(name="search",
         help="Print artefacts matching regular expression",
         options=storage_arguments() + expression_argument())
def search(args):
    """
    Search for artefacts matching the regular expression into bucket.
    :return:
    """
    storage = s3.S3Storage(args.storage_endpoint)
    matching_objects = storage.search(args.expression)

    if not matching_objects:
        LOGGER.warning("Did not found any matching folders/artefacts")
    else:
        print("\n".join(matching_objects))


def _ask_user(name, default):
    """
    Ask user for value for name, use default otherwise.
    """
    LOGGER.info("Missing artefact's {}".format(name))

    user_value = input("Please enter a value(default value \"{}\"):\n".format(
        default))

    return user_value if user_value else default


def _create_filter(names):
    """
    Create a filter function matching names.
    """
    if names == "*":
        return lambda k: False
    names = names.split("|")
    return lambda k: k not in names


def _prompt_missing_infos(artefact_object):
    """
    Prompt user for missing data in artefact.
    """
    filename = artefact_object.local_path if artefact_object.local_path else ""
    default_artefact = artefact.get_artefact_from_filename(filename)

    for attr in artefact.ATTRIBUTES:
        if not getattr(artefact_object, attr):
            user_value = _ask_user(name=attr,
                                   default=getattr(default_artefact, attr))
            setattr(artefact_object, attr, user_value)


def _user_confirm():
    """
    Ask user for confirmation before proceeding.
    """
    user_value = input("Are you sure? [y/N]?")

    return user_value.lower() == "y"
