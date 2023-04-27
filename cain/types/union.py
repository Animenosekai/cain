"""
union.py

Defines the union types.
"""
import typing

import cain.types
import cain.types.numbers as numbers
from cain import errors
from cain.model import Datatype

T = typing.TypeVarTuple("T")


class Union(Datatype, typing.Generic[*T]):
    """
    Handles the encoding and decoding of union elements (elements which can be of different types)
    """

    @classmethod
    def _encode(cls, value: typing.Union[*T], *args):
        current_type, _ = cain.types.retrieve_type(value.__class__)
        int_encoder = numbers.recommended_size(len(args))
        for index, arg in enumerate(args):
            arg_type, type_args = cain.types.retrieve_type(arg)
            if arg_type == current_type:
                return int_encoder._encode(index, *args) + arg_type._encode(value, *type_args)
        raise errors.EncodingError(cls,
                                   "The given element does not seem to be of any\
                                    type mentionned in the Union")

    @classmethod
    def _decode(cls, value: bytes, *args):
        int_encoder = numbers.recommended_size(len(args))
        type_index, value = int_encoder._decode(value, *args)
        current_type, type_args = cain.types.retrieve_type(args[type_index])
        return current_type._decode(value, *type_args)
