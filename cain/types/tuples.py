"""
tuples.py

Defines the Tuple datatype
"""
import typing

from cain.model import Datatype
from cain.types import Array

T = typing.TypeVarTuple("T")


class Tuple(Datatype, typing.Generic[*T]):
    """
    Handles the encoding and decoding of arrays.
    """

    @classmethod
    def _encode(cls, value: tuple[typing.Any], *args):
        return Array._encode(value, *args)

    @classmethod
    def _decode(cls, value: bytes, *args):
        data, value = Array._decode(value, *args)
        return tuple(data), value
