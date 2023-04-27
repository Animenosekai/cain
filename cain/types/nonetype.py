"""
sets.py

Defines the Set datatype
"""
import typing

from cain.model import Datatype


class NoneType(Datatype):
    """
    Handles the encoding and decoding of arrays.
    """

    @classmethod
    def _encode(cls, value: typing.Any, *args):
        return b""

    @classmethod
    def _decode(cls, value: bytes, *args):
        return None, value
