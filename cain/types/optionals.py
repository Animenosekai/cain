"""
optional.py

Defines the Optional datatype, which is used for optional values (which can be `None`).

Example
-------
>>> from cain.types import Optional
>>> Optional.encode("Hello world", str)
b'\x01Hello world\x00'
>>> Optional.decode(b'\x01Hello world\x00', str)
'Hello world'
>>> Optional.encode(None, str)
b'\x00'
>>> Optional.decode(b'\x00', str)
None

Structure
---------
`\x00` — Represents `None`
`\x01` + value encoded by Union — If the given value is not `None`,
                                  the value will be encoded using the `Union` datatype.
"""
import typing
import typing_extensions

import cain.types
from cain.model import Datatype

T = typing_extensions.TypeVarTuple("T")


class Optional(Datatype, typing.Generic[typing_extensions.Unpack[T]]):
    """
    Handles the encoding and decoding of optional elements.

    Example
    -------
    >>> Optional.encode("Hello world", str)
    b'\x01Hello world\x00'
    >>> Optional.decode(b'\x01Hello world\x00', str)
    'Hello world'
    >>> Optional.encode(None, str)
    b'\x00'
    >>> Optional.decode(b'\x00', str)
    None
    """

    @classmethod
    def _encode(cls, value: typing.Optional[typing.Any], *args):
        if value is None:
            return b"\x00"
        return b"\x01" + cain.types.Union._encode(value, *args)

    @classmethod
    def _decode(cls, value: bytes, *args):
        if value.startswith(b"\x00"):
            return None, value[1:]
        return cain.types.Union._decode(value[1:], *args)
