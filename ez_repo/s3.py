#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os.path import basename, join, realpath
import re

import boto3

from ez_repo.storage import Storage
from ez_repo.error import ExpressionError

S3_RESOURCE = boto3.resource("s3")


class S3Storage(Storage):
    """
    Class implementing a S3 storage device.
    """

    def __init__(self, endpoint):
        """
        Constructor.
        """
        Storage.__init__(self, endpoint)
        self.bucket = S3_RESOURCE.Bucket(self.endpoint)

    def _all_object_versions(self, name):
        versions_metadata = S3_RESOURCE.meta.client.list_object_versions(
            Bucket=self.bucket.name,
            Prefix=name
        )

        object_versions = []
        for version_metadata in versions_metadata["Versions"]:
            object_versions.append(version_metadata["VersionId"])
        return object_versions

    def delete(self, name):
        """
        Delete an artefact in the S3 bucket.
        """
        for version in self._all_object_versions(name):
            S3_RESOURCE.meta.client.delete_object(
                Bucket=self.bucket.name,
                Key=name,
                VersionId=version
            )

    def download(self, name):
        """
        Download artefact(s) matching regular expression from the bucket.
        """
        local_path = join(realpath("."), basename(name))
        self.bucket.download_file(name, local_path)

    def search(self, regular_expression):
        """
        Returns a list of object names matching regular expression.
        """
        return self._matching_objects(regular_expression).keys()

    def _matching_objects(self, regular_expression):
        """
        Returns a dict of matching objects (name, boto3 object).
        """
        try:
            re.compile(regular_expression)
        except re.error as e:
            raise ExpressionError(
                "\'{}\' is mal formatted. Reason: {}".format(
                    regular_expression,
                    e
                ))

        matching_objects = dict()
        for object in self.bucket.objects.all():
            if re.search(regular_expression, object.key):
                matching_objects[object.key] = object

        return matching_objects

    def upload(self, artefact):
        """
        Upload an artefact to S3.
        :param artefact:
        """
        data = open(artefact.local_path, 'rb')

        if artefact.repository == "release":
            storage_class = "STANDARD_IA"
        else:
            storage_class = "REDUCED_REDUNDANCY"

        metadata = artefact.get_metadata_map()
        metadata["classifiers"] = artefact.classifiers
        metadata["version"] = artefact.version

        self.bucket.put_object(
            Key=artefact.get_path(),
            Metadata=metadata,
            ContentDisposition="filename={}".format(artefact.get_dlname()),
            StorageClass=storage_class,
            Body=data
        )
