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

import typing_extensions

import cain.types
from cain import errors
from cain.model import Datatype
from cain.types import Array, Union

T = typing_extensions.TypeVarTuple("T")


class Set(Datatype, typing.Generic[typing_extensions.Unpack[T]]):
    """
    Handles the encoding and decoding of arrays.

    Example
    -------
    >>> Set.encode({"Hello", "world"}, str)
    b'\x00\x02\x00\x00Hello\x00world\x00'
    >>> Set.encode({"Hello", 1}, str, int)
    b'\x00Hello\x00\x00\x01'
    >>> Set.decode(b'\x00\x02\x00\x00Hello\x00world\x00', str)
    {'Hello', 'world'}
    >>> Set[str, int].decode(b'\x00Hello\x00\x00\x01')
    {'Hello', 1}
    """

    @staticmethod
    def preprocess_types(args):
        results = tuple()
        other_args = []

        for arg in args:
            try:
                current_type, args = cain.types.retrieve_type(arg)
                results += (current_type,)
            except (errors.UnknownTypeError, TypeError):
                other_args.append(arg)

        return [Union[results], *other_args]

    @classmethod
    def _encode(cls, value: set[typing.Any], *args):
        return Array._encode(value, *cls.preprocess_types(args))

    @classmethod
    def _decode(cls, value: bytes, *args):
        # Note: It is still relevant to compare for redundancies because multiple values
        # can have the same encoded value

        # TODO: Look for optimisations utilizing the fact that sets are unordered
        data, value = Array._decode(value, *cls.preprocess_types(args))
        return set(data), value
