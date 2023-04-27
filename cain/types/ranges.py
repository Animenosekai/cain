"""
range.py

Defines the Range datatype
"""
import typing

from cain.model import Datatype
import cain.types.numbers as numbers

T = typing.TypeVarTuple("T")


class Range(Datatype, typing.Generic[*T]):
    """
    Handles the encoding and decoding of ranges.
    """

    @classmethod
    def encode(cls, value: range, *args):
        args += (numbers.SHORT,)  # start with only 8 bits integers
        return numbers.Int.encode(value.start, *args) + numbers.Int.encode(value.stop, *args) + numbers.Int.encode(value.step, *args)

    @classmethod
    def decode(cls, value: bytes, *args):
        args += (numbers.SHORT,)  # start with only 8 bits integers
        start, value = numbers.Int.decode(value, *args)
        stop, value = numbers.Int.decode(value, *args)
        step, value = numbers.Int.decode(value, *args)
        return range(start, stop, step), value
