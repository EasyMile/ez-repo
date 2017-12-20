#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from os.path import join, basename, splitext

ATTRIBUTES = {
    "repository": "snapshot",
    "society": "easymile",
    "name": "",
    "version": "",
    "extension": "",
    "classifiers": "",
    "metadata": "",
    "local_path": ""
}

REPOSITORIES = [
    "release",
    "snapshot",
    "extern",
    "intern"
]


class Artefact(object):
    """
    Class defining an artefact properties.
    """

    def __init__(self, **kwargs):
        """
        Constructor
        """
        for (name, value) in kwargs.items():
            if name in ATTRIBUTES.keys():
                setattr(self, name, value)

        for attr in ATTRIBUTES:
            if attr not in self.__dict__.keys():
                setattr(self, attr, None)

    def get_metadata_map(self):
        metadata = dict()
        if self.metadata and ":" in self.metadata:
            for entry in self.metadata.split(";"):
                key, value = entry.split(":")
                metadata[key] = value[1]
        return metadata

    def get_artefact_name(self):
        return "{}-{}{}{}".format(
            self.name,
            self.version,
            "-" + self.classifiers if self.classifiers else "",
            self.get_file_ext(self.local_path))

    def get_dlname(self):
        dlname = "{}-{}{}".format(
            self.name,
            self.version,
            "-" + self.classifiers if self.classifiers else "")

        for value in self.get_metadata_map().values():
            dlname += "-{}".format(value)
        return dlname + self.get_file_ext(self.local_path)

    def missing_infos(self):
        missing = set()
        for (name, value) in self.__dict__.items():
            # Extension can be empty
            if name == "extension" and not value:
                continue
            elif value is None:
                missing.add(name)
            elif name not in ["classifiers", "metadata"] and value == "":
                missing.add(name)
        return missing

    def get_path(self):
        """

        :return:
        """
        parent_dir = join(self.repository,
                          self.society,
                          self.name,
                          self.version)

        return join(parent_dir, self.get_artefact_name())

    def get_file_ext(self, path):
        extension = self.extension
        if extension is None:
            extension = splitext(path)[1]
        elif extension and not extension.startswith("."):
            extension = "." + extension
        return extension


def get_artefact_from_filename(local_path):
    """

    :param artefact:
    :return:
    """
    file_name = basename(local_path)
    name = ""
    version = ""
    classifiers = ""

    # With classifiers
    m = re.match("([^-]+)-([0-9.]+)-([^.]+)\.(.+)", file_name)
    if m:
        name = m.group(1)
        version = m.group(2)
        classifiers = m.group(3)
    # Without
    else:
        m = re.match("([^-]+)-([0-9.]+)\.(.+)", file_name)
        if m:
            name = m.group(1)
            version = m.group(2)

    return Artefact(local_path=local_path,
                    repository=ATTRIBUTES["repository"],
                    society=ATTRIBUTES["society"],
                    name=name,
                    version=version,
                    classifiers=classifiers,
                    extension="",
                    metadata=ATTRIBUTES["metadata"])
