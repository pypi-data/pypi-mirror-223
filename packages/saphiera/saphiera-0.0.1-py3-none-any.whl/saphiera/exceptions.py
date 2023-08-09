# -*- coding: utf-8 -*-
"""All exceptions used in Spren are defined here."""


class SprenException(Exception):
    """
    Base exception class.

    All Spren-specific exceptions subclass this class.
    """


class InvalidSchemaDefinition(SprenException):
    """
    Error that is raised when constructing a schema.
    """
