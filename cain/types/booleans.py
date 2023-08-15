"""
booleans.py

Defines the Boolean datatype, which is used to store boolean values.

Example
-------
>>> from cain.types import Boolean
>>> b = Boolean(True)
>>> b.encoded
b'\x01'
>>> Boolean.encode(False)
b'\x00'
>>> Binary.decode(b'\x01')
True

Structure
---------
`\x01` — Represents `True`
`\x00` — Represents `False`
"""
from cain import errors
from cain.model import Datatype


class Boolean(Datatype):
    """
    Handles the encoding and decoding of booleans.

    Example
    -------
    >>> b = Boolean(True)
    >>> b.encoded
    b'\x01'
    >>> Boolean.encode(False)
    b'\x00'
    >>> Binary.decode(b'\x01')
    True
    """

    @classmethod
    def _encode(cls, value: int, *args):
        return b'\x01' if value else b'\x00'

    @classmethod
    def _decode(cls, value: bytes, *args):
        # could allow for booleans as integers or strings in `args` ?
        if value.startswith(b'\x00'):
            return False, value[1:]
        elif value.startswith(b'\x01'):
            return True, value[1:]
        raise errors.DecodingError(cls, "The given value does not seem to be a boolean")


Bool = Boolean
