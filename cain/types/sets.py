"""
sets.py

Defines the Set datatype
"""
import typing

from cain.model import Datatype
from cain.types import Array

T = typing.TypeVarTuple("T")


class Set(Datatype, typing.Generic[*T]):
    """
    Handles the encoding and decoding of arrays.
    """

    @classmethod
    def encode(cls, value: set[typing.Any], *args):
        return Array.encode(value, *args)

    @classmethod
    def decode(cls, value: bytes, *args):
        data, value = Array.decode(value, *args)
        return set(data), value
