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
    def _encode(cls, value: set[typing.Any], *args):
        return Array._encode(value, *args)

    @classmethod
    def _decode(cls, value: bytes, *args):
        data, value = Array._decode(value, *args)
        return set(data), value
