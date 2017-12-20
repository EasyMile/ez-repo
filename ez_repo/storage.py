#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Storage(object):
    """
    Class representing the interface of a storage device.
    """

    def __init__(self, endpoint):
        """
        Constructor taking the endpoint of the storage to use.
        """
        self.endpoint = endpoint

    def delete(self, regular_expression):
        """
        Delete artefacts in the current storage.
        """
        pass

    def download(self, regular_expression):
        """
        Download artefact(s) from the current storage.
        """
        pass

    def search(self, regular_expression):
        """
        Search artefacts in the storage.
        """
        pass

    def upload(self, artefact):
        """
        Upload artefact into the storage.
        """
        pass

    def multi_upload(self, artefacts):
        """
        Upload multiple artefacts into the storage.
        """
        for artefact in artefacts:
            self.upload(artefact)
