#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ez_repo.artefact as aa


def _artefact_data(
        repository="",
        society="",
        name="",
        version="",
        classifiers="",
        extension="",
        metadata="",
        local_path=""):
    return {
        "repository": repository,
        "society": society,
        "name": name,
        "version": version,
        "classifiers": classifiers,
        "extension": extension,
        "metadata": metadata,
        "local_path": local_path
    }


def _simple_data():
    data = _artefact_data(
        repository="release",
        society="enterprise",
        name="name",
        version="1.0.0",
        classifiers="Test",
        extension="tst",
        metadata="meta:data",
        local_path="temp/file")

    artefact = aa.Artefact(
        repository=data["repository"],
        society=data["society"],
        name=data["name"],
        version=data["version"],
        classifiers=data["classifiers"],
        extension=data["extension"],
        metadata=data["metadata"],
        local_path=data["local_path"])

    return data, artefact


def test_artefact():
    data, artefact = _simple_data()

    for key, value in data.items():
        assert getattr(artefact, key) == value


# def test_partial_args_get_path():
#     data = _artefact_data(
#         repository="release",
#         society="enterprise",
#         name="name",
#         extension="tst",
#         metadata="meta;data",
#         local_path="temp/file")

#     artefact = aa.Artefact(
#         repository=data["repository"],
#         society=data["society"],
#         name=data["name"],
#         extension=data["extension"],
#         local_path=data["local_path"])

#     assert artefact.get_path() == join(
#         data["repository"],
#         data["society"],
#         data["name"])


# def test_get_path():
#     data, artefact = _simple_data()

#     assert artefact.get_path() == join(
#         data["repository"],
#         data["society"],
#         data["name"],
#         data["version"])


# def test_get_artefact_with_classifiers_from_filename():
#     file_path = "/tmp/name-1.0.0-Test.zip"
#     artefact = aa.get_artefact_from_filename(file_path)

#     assert artefact.s3path == aa.DEFAULT_PATH + "name"
#     assert artefact.s3name == "name-1.0.0-Test.zip"
#     assert artefact.version == "1.0.0"
#     assert artefact.classifiers == "Test"
#     assert artefact.extension == "zip"


# def test_get_artefact_without_classifiers_from_filename():
#     file_path = "/tmp/name-1.0.0.zip"
#     artefact = aa.get_artefact_from_filename(file_path)

#     assert artefact.s3path == aa.DEFAULT_PATH + "name"
#     assert artefact.s3name == "name-1.0.0.zip"
#     assert artefact.version == "1.0.0"
#     assert artefact.extension == "zip"
