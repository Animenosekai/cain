"""
union.py

Defines the union types.
"""
import typing

import cain.types.numbers as numbers
from cain import errors
from cain.model import Datatype
import cain.types

T = typing.TypeVarTuple("T")


class Union(Datatype, typing.Generic[*T]):
    """
    Handles the encoding and decoding of union elements (elements which can be of different types)
    """

    @classmethod
    def encode(cls, value: typing.Union[*T], *args):
        current_type, _ = cain.types.retrieve_type(value.__class__)
        for index, arg in enumerate(args):
            arg_type, type_args = cain.types.retrieve_type(arg)
            if arg_type == current_type:
                return numbers.Int.encode(index, *args) + arg_type.encode(value, *type_args)
        raise errors.EncodingError(cls, "The given element does not seem to be of any type mentionned in the Union")

    @classmethod
    def decode(cls, value: bytes, *args):
        type_index, value = numbers.Int.decode(value, *args)
        current_type, type_args = cain.types.retrieve_type(args[type_index])
        return current_type.decode(value, *type_args)
