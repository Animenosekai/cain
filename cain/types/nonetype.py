"""
nonetype.py

Defines the NoneType datatype, which is used to store `None`.

Example
-------
>>> from cain.types import NoneType
>>> n = NoneType(None)
>>> n.encoded
b''
>>> NoneType.encode(None)
b''
>>> NoneType.decode(b'')
None

Structure
---------
Nothing is appended, because the value does not change,\
we only need to know that it is `None`/`null`.
"""
import typing

from cain.model import Datatype


class NoneType(Datatype):
    """
    Handles the encoding and decoding of arrays.

    Example
    -------
    >>> n = NoneType(None)
    >>> n.encoded
    b''
    >>> NoneType.encode(None)
    b''
    >>> NoneType.decode(b'')
    None
    """

    @classmethod
    def _encode(cls, value: typing.Any, *args):
        return b""

    @classmethod
    def _decode(cls, value: bytes, *args):
        return None, value
