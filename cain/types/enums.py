"""
enums.py

Defines the Enum datatype, which is used for enumerations.

Example
-------
>>> from cain.types import Enum
>>> Enum["hello", "world"].encode("hello")
b'\x00'
>>> Enum["hello", "world"].decode("\x00")
"hello"

Structure
---------
The `encode` function returns the index of the type argument.
Note: The type arguments are sorted.
"""
import typing

import cain.types.numbers as numbers
from cain.model import Datatype


class Enum(Datatype):
    """
    Handles the encoding and decoding of enums.

    Example
    -------
    >>> Enum["hello", "world"].encode("hello")
    b'\x00'
    >>> Enum["hello", "world"].decode(b"\x00")
    "hello"
    """

    @classmethod
    def _encode(cls, value: typing.Any, *args):
        args = sorted(args)
        int_encoder = numbers.recommended_size(len(args))

        for index, arg in enumerate(args):
            if arg == value:
                return int_encoder._encode(index)

        raise ValueError(f"Tried to encode value `{value}` which isn't in the enum `{cls}`")

    @classmethod
    def _decode(cls, value: bytes, *args):
        args = sorted(args)
        int_encoder = numbers.recommended_size(len(args))
        arg_index, value = int_encoder._decode(value, *args)
        return args[arg_index], value
