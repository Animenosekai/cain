"""
binary.py

Defines the Binary datatype
"""
import typing
from cain.model import Datatype

long = LONG = Long = "long"
short = SHORT = Short = "short"

T = typing.TypeVarTuple("T")

class Binary(Datatype, typing.Generic[*T]):
    """
    Handles the encoding and decoding of binary blob.
    """

    @staticmethod
    def process_args(args):
        """
        Returns the right blob length size
        """
        size = 4
        for arg in args:
            if arg == long:
                size += 2
            elif arg == short:
                size -= 2
        return size

    @classmethod
    def encode(cls, value: bytes, *args):
        # length of blob + blob
        len_size = cls.process_args(args)
        return len(value).to_bytes(len_size) + value

    @classmethod
    def decode(cls, value: bytes, *args):
        len_size = cls.process_args(args)
        blob_size = int.from_bytes(value[:len_size])
        return value[len_size:len_size + blob_size], value[len_size + blob_size:]
