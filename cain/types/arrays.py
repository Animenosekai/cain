"""
arrays.py

Defines the Array datatype
"""
import typing
from cain.model import Datatype
from cain.types import retrieve_type, Int

T = typing.TypeVarTuple("T")


class Array(Datatype, typing.Generic[*T]):
    """
    Handles the encoding and decoding of arrays.
    """

    @staticmethod
    def process_args(args):
        """
        Returns the right blob length size
        """
        return None

    @classmethod
    def encode(cls, value: list[typing.Any], *args):
        length = len(value)

        return b""

    @classmethod
    def decode(cls, value: bytes, *args):
        return b"", value
