"""
optional.py

Defines the optional types.
"""
import typing

import cain.types.union as union
from cain.model import Datatype
import cain.types

T = typing.TypeVarTuple("T")


class Optional(Datatype, typing.Generic[*T]):
    """
    Handles the encoding and decoding of optional elements.
    """

    @classmethod
    def encode(cls, value: typing.Optional[typing.Any], *args):
        if value is None:
            return b"\x00"
        if len(args) == 1:
            current_type, type_args = cain.types.retrieve_type(args[0])
            return b"\x01" + current_type.encode(value, *type_args)
        return b"\x01" + union.Union.encode(value, *args)

    @classmethod
    def decode(cls, value: bytes, *args):
        if value.startswith(b"\x00"):
            return None, value[1:]
        value = value[1:]
        if len(args) == 1:
            current_type, type_args = cain.types.retrieve_type(args[0])
            return current_type.decode(value, *type_args)
        return union.Union.decode(value, *args)
