"""
binary.py

Defines the Binary datatype, which is used to store binary data.

Example
-------
>>> from cain.types import Binary
>>> b = Binary(b"Hello world")
>>> b.encoded
b'\x00\x00\x00\x0bHello world'
>>> Binary.encode(b"Hello world")
b'\x00\x00\x00\x0bHello world'
>>> Binary.decode(b"\x00\x00\x00\x0bHello world")
b'Hello world'
>>> Binary.encode(b"Hello world", "long")
b'\x00\x00\x00\x00\x0bHello world'
>>> Binary.decode(b"\x00\x00\x00\x00\x0bHello world", "long")
b'Hello world'

Structure
---------
\x00\x00\x00\x0b \x48\x65\x6c\x6c\x6f\x20\x77\x6f\x72\x6c\x64
~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  size of blob                   blob itself
"""
import typing
import typing_extensions

from cain.model import Datatype

# Type Arguments
long = LONG = Long = "long"
short = SHORT = Short = "short"

T = typing_extensions.TypeVarTuple("T")


class Binary(Datatype, typing.Generic[typing_extensions.Unpack[T]]):
    """
    Handles the encoding and decoding of binary blob.

    Note: the binary size integer is stored in 4 bytes by default, which is good for up to ~4.3 GB of data.

    Parameters
    ----------
    short
        Increases the size of the integer used to store the binary size by 1 byte.
    long
        Decreases the size of the integer used to store the binary size by 1 byte.

    Example
    -------
    >>> class A(Object):
    ...     a: Binary[LONG] # Will be able to take binary blobs as big as 1,099,511,627,776 bytes (~1100 GB) long.
    ...     b: Binary[SHORT] # Will be able to take binary blobs as big as 16,777,216 bytes (~17 MB) long.
    >>> Binary.encode(b"Hello world")
    b'\x00\x00\x00\x0bHello world'
    >>> Binary.decode(b"\x00\x00\x00\x0bHello world")
    b'Hello world'
    """

    @staticmethod
    def process_args(args):
        """
        Returns the right blob length size

        Parameters
        ----------
        tuple[str]
            The arguments given by the developer.

        Example
        -------
        >>> Binary.process_args((LONG, SHORT))
        4
        >>> Binary.process_args((LONG,))
        6
        >>> Binary.process_args((SHORT,))
        2
        >>> Binary.process_args(())
        4

        Returns
        -------
        int
            The size of the blob length integer.
        """
        size = 4  # default to 4 bytes (32-bit) unsigned integers which covers the 0 to 4,294,967,295 range.
        for arg in args:
            if arg == long:
                size += 1
            elif arg == short:
                size -= 1
        return size

    @classmethod
    def _encode(cls, value: bytes, *args):
        len_size = cls.process_args(args)
        # length of blob + blob itself
        return len(value).to_bytes(len_size, signed=False, byteorder="big") + value

    @classmethod
    def _decode(cls, value: bytes, *args):
        len_size = cls.process_args(args)
        blob_size = int.from_bytes(value[:len_size], signed=False, byteorder="big")  # getting the length first
        return value[len_size:len_size + blob_size], value[len_size + blob_size:]  # decoding the appropriate length
