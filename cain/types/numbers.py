"""
numbers.py

Defines the different Number datatypes.

Example
-------
>>> from cain.types import Number
>>> n = Number(3.14)
>>> n.encoded
b'\x1f\x85\xebQ\xb8\x1e\t@'
>>> Number.encode(3.14)
b'\x1f\x85\xebQ\xb8\x1e\t@'
>>> Number.decode(b'\x1f\x85\xebQ\xb8\x1e\t@')
3.14
>>> from cain.types import Int, Float
>>> Float.encode(3.14)
b'\xc3\xf5H@'
>>> Int.encode(3)
b'\x00\x03'
>>> Int.encode(3, "short")
b'\x03'
>>> Int.encode(3, "long")
b'\x00\x00\x03'

Structure
---------
Floating point numbers are encoded following IEEE 754.
They are separated into single precision (`Float`) and double precision (`Double`) numbers.

Decimals (`Decimal`) are exact representations of decimal numbers,
without any approximations. They are encoded as strings.

Complex numbers are encoded as two consecutive floats (`Complex`) or doubles (`DoubleComplex`).

Integers are encoded by turning them into without using any approximation,
converting them from base10 to base2.

When using the base `Int` class, you can modulate the range of encodable integers using
the `short`, `long`, `signed` and `unsigned` parameters.

You can also use the different fixed size classes (`Int64`, `UInt32`, etc.)
to save time on the arguments processing.

Refer to the different implementations for more information.
"""
import struct
import typing
import typing_extensions
import decimal

from cain.types import String
from cain.model import Datatype

# Type Arguments

# pylint: disable=invalid-name
signed = SIGNED = Signed = "signed"
unsigned = UNSIGNED = Unsigned = "unsigned"

long = LONG = Long = "long"
short = SHORT = Short = "short"

T = typing_extensions.TypeVarTuple("T")

# Number parent class


class Number(Datatype):
    """
    The default number class.

    Represents a double precision floating point number, encoded with 64 bits (8 bytes).
    The numbers can range from -1.7e308 to +1.7e308

    Example
    -------
    >>> n = Number(3.14)
    >>> n.encoded
    b'\x1f\x85\xebQ\xb8\x1e\t@'
    >>> Number.encode(3.14)
    b'\x1f\x85\xebQ\xb8\x1e\t@'
    >>> Number.decode(b'\x1f\x85\xebQ\xb8\x1e\t@')
    3.14
    """

    @classmethod
    def _encode(cls, value: float, *args):
        return struct.pack('d', float(value))

    @classmethod
    def _decode(cls, value: bytes, *args):
        [val] = struct.unpack('d', value[:8])
        return val, value[8:]

# FLOATING POINT NUMBERS


class Float(Number):
    """
    Represents a single precision floating point number, encoded with 32 bits (4 bytes).

    The numbers can range from -3.4e38 to 3.4e38

    Example
    -------
    >>> from cain.types import Int, Float
    >>> Float.encode(3.14)
    b'\xc3\xf5H@'
    """

    @classmethod
    def _encode(cls, value: float, *args):
        return struct.pack('f', float(value))

    @classmethod
    def _decode(cls, value: bytes, *args):
        [val] = struct.unpack('f', value[:4])
        return val, value[4:]


class Double(Number):
    """
    Represents a double precision floating point number, encoded with 64 bits (8 bytes).

    The numbers can range from -1.7e308 to +1.7e308
    """


class Decimal(Number):
    """
    Exact representation of a decimal number, no approximation or range is needed.
    """
    @classmethod
    def _encode(cls, value: typing.Union[str, decimal.Decimal], *args):
        return String._encode(str(value), *args)

    @classmethod
    def _decode(cls, value: bytes, *args):
        result, value = String._decode(value, *args)
        return decimal.Decimal(result), value


class Complex(Number):
    """
    Represents a complex number, encoded with 2*32 bits (2*4 bytes).
    """

    @classmethod
    def _encode(cls, value: complex, *args):
        return struct.pack('ff', value.real, value.imag)

    @classmethod
    def _decode(cls, value: bytes, *args):
        [real, imag] = struct.unpack('ff', value[:8])
        return complex(real, imag), value[8:]


class DoubleComplex(Number):
    """
    Represents a complex number, encoded with 2*64 bits (2*8 bytes).
    """

    @classmethod
    def _encode(cls, value: complex, *args):
        return struct.pack('dd', value.real, value.imag)

    @classmethod
    def _decode(cls, value: bytes, *args):
        [real, imag] = struct.unpack('dd', value[:16])
        return complex(real, imag), value[16:]

# Integers


class Int(Number, typing.Generic[typing_extensions.Unpack[T]]):
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
        Adds 1 byte to the size of the integer, allowing for greater ranges (can be used multiple times)
    short
        Removes 1 byte from the size of the integer, allowing for smaller ranges (can be used multiple times)

    Example
    -------
    >>> Int.encode(3)
    b'\x00\x03'
    >>> Int.encode(3, "short")
    b'\x03'
    >>> Int[long].encode(3)
    b'\x00\x00\x03'
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
                size += 1
            elif arg == SHORT:
                size -= 1

        return signed, size

    @classmethod
    def _encode(cls, value: int, *args):
        signed, size = cls.process_args(args)
        return int(value).to_bytes(size, signed=signed, byteorder="big")

    @classmethod
    def _decode(cls, value: bytes, *args):
        signed, size = cls.process_args(args)
        return int.from_bytes(value[:size], signed=signed, byteorder="big"), value[size:]


Integer = Int


class SignedInt(Int):
    """
    Represents a signed integer

    Note: By default, the size of the encoded integers is 2 bytes.
    Note: This is the same as `Int`, but the sign won't be checked while processing the args.
    """

    @staticmethod
    def process_args(args):
        size = 2

        for arg in args:
            if arg == LONG:
                size += 1
            elif arg == SHORT:
                size -= 1

        return True, size


signedint = SignedInt


class UnsignedInt(Int):
    """
    Represents a unsigned integer

    Note: By default, the size of the encoded integers is 2 bytes.
    Note: This is the same as `Int`, but the sign won't be checked while processing the args.
    """

    @staticmethod
    def process_args(args):
        size = 2

        for arg in args:
            if arg == LONG:
                size += 1
            elif arg == SHORT:
                size -= 1

        return False, size


uint = UInt = UnsignedInt


class Int8(Int):
    """
    Represents an 8-bit (1 byte) signed integer

    Note: Can store numbers in the -128 to 127 range.
    """

    @staticmethod
    def process_args(args):
        return True, 1


SignedInt8 = int8_t = int8 = Int8


class UInt8(Int):
    """
    Represents an 8-bit (1 byte) unsigned integer

    Note: Can store numbers in the 0 to 255 range.
    """

    @staticmethod
    def process_args(args):
        return False, 1


UnsignedInt8 = uint8_t = uint8 = UInt8


class Int16(Int):
    """
    Represents an 16-bit (2 bytes) signed integer

    Note: Can store numbers in the -32,768 to 32,767 range.
    """

    @staticmethod
    def process_args(args):
        return True, 2


SignedInt16 = int16_t = int16 = Int16


class UInt16(Int):
    """
    Represents an 16-bit (2 bytes) unsigned integer

    Note: Can store numbers in the 0 to 65,535 range.
    """

    @staticmethod
    def process_args(args):
        return False, 2


UnsignedInt16 = uint16_t = uint16 = UInt16


class Int32(Int):
    """
    Represents an 32-bit (4 bytes) signed integer

    Note: Can store numbers in the -2,147,483,648 to 2,147 483,647 range.
    """

    @staticmethod
    def process_args(args):
        return True, 4


SignedInt32 = int32_t = int32 = Int32


class UInt32(Int):
    """
    Represents an 32-bit (4 bytes) unsigned integer

    Note: Can store numbers in the 0 to 4,294,967,295 range.
    """

    @staticmethod
    def process_args(args):
        return False, 4


UnsignedInt32 = uint32_t = uint32 = UInt32


class Int64(Int):
    """
    Represents an 64-bit (8 bytes) signed integer

    Note: Can store numbers in the -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807 range.
    """

    @staticmethod
    def process_args(args):
        return True, 8


SignedInt64 = int64_t = int64 = Int64


class UInt64(Int):
    """
    Represents an 64-bit(8 bytes) unsigned integer

    Note: Can store numbers in the 0 to 18,446,744,073,709,551,615 range.
    """

    @staticmethod
    def process_args(args):
        return False, 8


UnsignedInt64 = uint64_t = uint64 = UInt64


def recommended_size(number: int, signed: bool = False) -> typing.Type[Int]:
    """
    Returns the recommended integer encoder for the given number

    Parameters
    ----------
    number: int
        The integer to encode
    signed: bool, default = False
        Whether to consider a signed encoder or not. If the value is negative, it will be infered.

    Returns
    -------
    Int
        The encoder to use

    Raises
    ------
    ValueError
        If the given value is too big to be encoded within 8 bytes
    """
    if signed or number < 0:
        if -128 <= number <= 127:
            return Int8
        elif -32_768 <= number <= 32_767:
            return Int16
        elif -2_147_483_648 <= number <= 2_147_483_647:
            return Int32
        elif -9_223_372_036_854_775_808 <= number <= 9_223_372_036_854_775_807:
            return Int64
        raise ValueError("The number is too big to be encoded as a signed integer")
    if number <= 255:
        return UInt8
    elif number <= 65_535:
        return UInt16
    elif number <= 4_294_967_295:
        return UInt32
    elif number <= 18_446_744_073_709_551_615:
        return UInt64
    raise ValueError("The number is too big to be encoded as an unsigned integer")
