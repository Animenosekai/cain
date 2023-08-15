"""
tuples.py

Defines the Tuple datatype, which is used to store tuples.

Example
-------
>>> from cain.types import Tuple
>>> Tuple.encode(("Hello", "world"), str)
b'\x00\x02\x00\x00Hello\x00world\x00'
>>> Tuple.encode(("Hello", 1), str, int)
b'\x00Hello\x00\x00\x01'
>>> Tuple.decode(b'\x00\x02\x00\x00Hello\x00world\x00', str)
('Hello', 'world')
>>> Tuple.decode(b'\x00Hello\x00\x00\x01', str, int)
('Hello', 1)

Structure
---------
Under the hood, Tuples are encoded the same as Arrays.
Refer to `Array` for more information.
"""
import typing
import typing_extensions

from cain.model import Datatype
from cain.types import Array

T = typing_extensions.TypeVarTuple("T")


class Tuple(Datatype, typing.Generic[typing_extensions.Unpack[T]]):
    """
    Handles the encoding and decoding of tuples.

    Example
    -------
    >>> Tuple.encode(("Hello", "world"), str)
    b'\x00\x02\x00\x00Hello\x00world\x00'
    >>> Tuple.encode(("Hello", 1), str, int)
    b'\x00Hello\x00\x00\x01'
    >>> Tuple.decode(b'\x00\x02\x00\x00Hello\x00world\x00', str)
    ('Hello', 'world')
    >>> Tuple[str, int].decode(b'\x00Hello\x00\x00\x01')
    ('Hello', 1)
    """

    @classmethod
    def _encode(cls, value: tuple[typing.Any], *args):
        return Array._encode(value, *args)

    @classmethod
    def _decode(cls, value: bytes, *args):
        data, value = Array._decode(value, *args)
        return tuple(data), value
