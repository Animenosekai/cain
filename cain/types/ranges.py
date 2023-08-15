"""
ranges.py

Defines the Range datatype, which is used to store `range` objects.

Note: `range` objects are Python objects which are iterables
      giving whole numbers between two boundaries (`start` and `stop`) using a given `step`.

Example
-------
>>> from cain.types import Range
>>> r = Range(range(0, 4, 2))
>>> r.encoded
b'\x00\x04\x02'
>>> Range.encode(range(0, 4, 2))
b'\x00\x04\x02'
>>> Range.decode(b'\x00\x04\x02')
range(0, 4, 2)
>>> for i in Range.decode(b'\x00\x04\x02'):
...     print(i)
0
2

Structure
---------
\x00 \x04 \x02
 (1)  (2)  (3)

(1): The start of the range.
(2): The end of the range.
(3): The step of the range.

Note: The integers used by default are unsigned 8-bit integers (covering the -128 to 127 range).
      You can use the same type arguments as `Int` to change this behaviour.
      Refer to `Int` for more information.
"""
import typing
import typing_extensions

import cain.types.numbers as numbers
from cain.model import Datatype

T = typing_extensions.TypeVarTuple("T")


class Range(Datatype, typing.Generic[typing_extensions.Unpack[T]]):
    """
    Handles the encoding and decoding of ranges.

    Example
    -------
    >>> r = Range(range(0, 4, 2))
    >>> r.encoded
    b'\x00\x04\x02'
    >>> Range.encode(range(0, 4, 2))
    b'\x00\x04\x02'
    >>> Range.decode(b'\x00\x04\x02')
    range(0, 4, 2)
    >>> for i in Range.decode(b'\x00\x04\x02'):
    ...     print(i)
    0
    2
    """

    @classmethod
    def _encode(cls, value: range, *args):
        args += (numbers.SHORT,)  # start with only 8 bits integers
        return numbers.Int._encode(value.start, *args) + numbers.Int._encode(value.stop, *args) + numbers.Int._encode(value.step, *args)

    @classmethod
    def _decode(cls, value: bytes, *args):
        args += (numbers.SHORT,)  # start with only 8 bits integers
        start, value = numbers.Int._decode(value, *args)
        stop, value = numbers.Int._decode(value, *args)
        step, value = numbers.Int._decode(value, *args)
        return range(start, stop, step), value
