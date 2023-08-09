# -*- coding: utf-8 -*-
import enum
from typing import Any


class MetaEnum(enum.EnumMeta):
    def __contains__(cls, member: Any) -> bool:
        if type(member) == cls:
            return enum.EnumMeta.__contains__(cls, member)
        else:
            try:
                cls(member)
            except ValueError:
                return False
            return True


class Enum(enum.Enum, metaclass=MetaEnum):
    """A custom Enum that allows for checking if a value exists, using
    `{value} in {Enum}`

    class Foo(Enum):
        foo = 1
        bar = 5

    >>> 1 in Foo
    True

    >>> Foo.bar in Foo
    True

    >>> 2 in Foo
    False
    """

    pass
