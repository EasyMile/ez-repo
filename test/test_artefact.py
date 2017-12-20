#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import join

import artefact.artefact as aa


def _artefact_data(
        repository="",
        path="",
        name="",
        version="",
        classifiers="",
        extension="",
        local_path=""):
    return {
        "repository": repository,
        "s3path": path,
        "s3name": name,
        "version": version,
        "classifiers": classifiers,
        "extension": extension,
        "local_path": local_path
    }


def _simple_data():
    data = _artefact_data(
        repository="release",
        path="enterprise/artefact",
        name="name",
        version="1.0.0",
        classifiers="Test",
        extension="tst",
        local_path="temp/file")

    artefact = aa.Artefact(
        repository=data["repository"],
        path=data["s3path"],
        name=data["s3name"],
        version=data["version"],
        classifiers=data["classifiers"],
        extension=data["extension"],
        local_path=data["local_path"])

    return data, artefact


def test_artefact():
    data, artefact = _simple_data()

    for key, value in data.items():
        assert getattr(artefact, key) == value


def test_partial_args_get_s3_path():
    data = _artefact_data(
        repository="release",
        path="enterprise/artefact",
        name="name",
        extension="tst",
        local_path="temp/file")

    artefact = aa.Artefact(
        repository=data["repository"],
        path=data["s3path"],
        name=data["s3name"],
        extension=data["extension"],
        local_path=data["local_path"])

    assert artefact.get_s3_path() == join(
        data["repository"],
        data["s3path"],
        data["s3name"])


def test_get_s3_path():
    data, artefact = _simple_data()

    assert artefact.get_s3_path() == join(
        data["repository"],
        data["s3path"],
        data["version"],
        data["s3name"])


def test_get_artefact_with_classifiers_from_filename():
    file_path = "/tmp/name-1.0.0-Test.zip"
    artefact = aa.get_artefact_from_filename(file_path)

    assert artefact.s3path == aa.DEFAULT_PATH + "name"
    assert artefact.s3name == "name-1.0.0-Test.zip"
    assert artefact.version == "1.0.0"
    assert artefact.classifiers == "Test"
    assert artefact.extension == "zip"


def test_get_artefact_without_classifiers_from_filename():
    file_path = "/tmp/name-1.0.0.zip"
    artefact = aa.get_artefact_from_filename(file_path)

    assert artefact.s3path == aa.DEFAULT_PATH + "name"
    assert artefact.s3name == "name-1.0.0.zip"
    assert artefact.version == "1.0.0"
    assert artefact.extension == "zip"
