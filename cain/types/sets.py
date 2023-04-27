"""
sets.py

Defines the Set datatype, which is used to store sets (unordered).

Example
-------
>>> from cain.types import Set
>>> Set.encode({"Hello", "world"}, str)
b'\x00\x02\x00\x00Hello\x00world\x00'
>>> Set.encode({"Hello", 1}, str, int)
b'\x00Hello\x00\x00\x01'
>>> Set.decode(b'\x00\x02\x00\x00Hello\x00world\x00', str)
{'Hello', 'world'}
>>> Set.decode(b'\x00Hello\x00\x00\x01', str, int)
{'Hello', 1}

Structure
---------
Under the hood, Sets are encoded the same as Arrays.
Refer to `Array` for more information.
"""
import typing

from cain.model import Datatype
from cain.types import Array

T = typing.TypeVarTuple("T")


class Set(Datatype, typing.Generic[*T]):
    """
    Handles the encoding and decoding of arrays.
    """

    @classmethod
    def _encode(cls, value: set[typing.Any], *args):
        return Array._encode(value, *args)

    @classmethod
    def _decode(cls, value: bytes, *args):
        # TODO: Look for optimisations utilizing the fact that sets are unordered
        data, value = Array._decode(value, *args)
        return set(data), value
