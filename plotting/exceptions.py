#!/bin/env python
"""
Put module documentation here
"""


class MissingArgumentException(Exception):
    def __init__(self, missing_fields: list):
        self.missing_fields = missing_fields

    def __str__(self):
        return "Missing arguments: {}".format(",".join(self.missing_fields))

    def __repr__(self):
        return self.__str__()
