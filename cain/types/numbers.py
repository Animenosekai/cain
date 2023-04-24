"""
numbers.py

Defines the different number representations.
"""
import struct
import typing

from cain.model import Datatype

# Type Arguments

# pylint: disable=invalid-name
signed = SIGNED = Signed = "signed"
unsigned = UNSIGNED = Unsigned = "unsigned"

long = LONG = Long = "long"
short = SHORT = Short = "short"

T = typing.TypeVarTuple("T")

# Number parent class


class Number(Datatype):
    """
    The default number class.

    Represents a double precision floating point number, encoded with 64 bits (8 bytes).
    The numbers can range from -1.7e308 to +1.7e308
    """

    @classmethod
    def encode(cls, value: float, *args):
        return struct.pack('d', float(value))

    @classmethod
    def decode(cls, value: bytes, *args):
        [val] = struct.unpack('d', value[:8])
        return val, value[8:]


class Int(Number, typing.Generic[*T]):
    """
    Represents an integer

    Note: By default, the size of the encoded integers is 2 bytes.

    Note: When the `signed` and `unsigned` parameters are used multiple times, the last one is used.

    Parameters
    ----------
    signed, default
        When using signed integers.
    unsigned
        When the sign is not important, the range of encodable numbers is greater
    long
        Adds 2 bytes to the size of the integer, allowing for greater ranges (can be used multiple times)
    short
        Removes 2 bytes from the size of the integer, allowing for smaller ranges (can be used multiple times)
    """

    @staticmethod
    def process_args(args):
        """
        Returns the right size and sign of the processing numbers
        """
        signed = True
        size = 2

        for arg in args:
            if arg == SIGNED:
                signed = True
            elif arg == UNSIGNED:
                signed = False
            elif arg == LONG:
                size += 2
            elif arg == SHORT:
                size -= 2

        return signed, size

    @classmethod
    def encode(cls, value: int, *args):
        signed, size = cls.process_args(args)
        return int(value).to_bytes(size, signed=signed)

    @classmethod
    def decode(cls, value: bytes, *args):
        signed, size = cls.process_args(args)
        return int.from_bytes(value[:size], signed=signed), value[size:]


class Double(Number):
    """
    Represents a double precision floating point number, encoded with 64 bits (8 bytes).

    The numbers can range from -1.7e308 to +1.7e308
    """


class Float(Number):
    """
    Represents a single precision floating point number, encoded with 32 bits (4 bytes).

    The numbers can range from -3.4e38 to 3.4e38
    """

    @classmethod
    def encode(cls, value: int, *args):
        return struct.pack('f', float(value))

    @classmethod
    def decode(cls, value: bytes, *args):
        [val] = struct.unpack('f', value[:4])
        return val, value[4:]
