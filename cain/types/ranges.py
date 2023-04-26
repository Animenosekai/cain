"""
range.py

Defines the Range datatype
"""
import typing

from cain.model import Datatype
from cain.types import Int

T = typing.TypeVarTuple("T")


class Range(Datatype, typing.Generic[*T]):
    """
    Handles the encoding and decoding of ranges.
    """

    @classmethod
    def encode(cls, value: range, *args):
        return Int.encode(value.start, *args) + Int.encode(value.stop, *args) + Int.encode(value.step, *args)

    @classmethod
    def decode(cls, value: bytes, *args):
        start, value = Int.decode(value, *args)
        stop, value = Int.decode(value, *args)
        step, value = Int.decode(value, *args)
        return range(start, stop, step), value
