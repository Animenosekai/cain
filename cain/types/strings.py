"""
strings.py

Defines the strings datatype.
"""
import typing

import cain.types.characters as characters
from cain import errors
from cain.model import Datatype

T = typing.TypeVarTuple("T")


class String(Datatype, typing.Generic[*T]):
    """
    Handles the encoding and decoding of binary blob.
    """

    @classmethod
    def encode(cls, value: str, *args):
        # length of blob + blob
        data = b""
        for letter in value:
            data += characters.Character.encode(letter, *args)
        data += b"\x00"
        return data

    @classmethod
    def decode(cls, value: bytes, *args):
        result = ""
        counter = 0
        value_len = len(value)
        while not value.startswith(b"\x00"):
            if counter >= value_len:  # avoiding infinite loops
                raise errors.DecodingError(cls, "Unterminated string")
            letter, value = characters.Character.decode(value, *args)
            result += letter
            counter += 1
        return result, value[1:]  # value contains "\x00" at its start
