"""
strings.py

Defines the String datatype, which is used to store strings.

Example
-------
>>> from cain.types import String
>>> s = String("Hello world")
>>> s.encoded
b'Hello world\x00'
>>> String.encode("夏祭り")
b'\xe5\xa4\x8f\xe7\xa5\xad\xe3\x82\x8a\x00'
>>> String.decode(b'\xe5\xa4\x8f\xe7\xa5\xad\xe3\x82\x8a\x00')
'夏祭り'

Structure
---------
Each character is encoded using `Character` and the string ends with a NULL character (`\x00`).
Refer to `Character` for more information.
"""

import cain.types.characters as characters
from cain import errors
from cain.model import Datatype


class String(Datatype):
    """
    Handles the encoding and decoding of strings.

    Example
    -------
    >>> s = String("Hello world")
    >>> s.encoded
    b'Hello world\x00'
    >>> String.encode("夏祭り")
    b'\xe5\xa4\x8f\xe7\xa5\xad\xe3\x82\x8a\x00'
    >>> String.decode(b'\xe5\xa4\x8f\xe7\xa5\xad\xe3\x82\x8a\x00')
    '夏祭り'
    """

    @classmethod
    def _encode(cls, value: str, *args):
        data = b""
        for letter in value:
            # encoding each letter
            data += characters.Character._encode(letter, *args)
        data += b"\x00"  # appending a NULL character to notify the end of the string
        return data

    @classmethod
    def _decode(cls, value: bytes, *args):
        # Warning: This method only works because `characters.Character` only uses UTF-8
        term = value.find(b"\x00")
        if term == -1:
            raise errors.DecodingError(cls, "Unterminated string")
        try:
            return value[:term].decode("utf-8"), value[term + 1:]
        except UnicodeDecodeError:
            pass

        # Falling back to the old method
        result = ""
        for letter in value:
            if value.startswith(b"\x00"):
                break
            letter, value = characters.Character._decode(value, *args)
            result += letter
        else:
            raise errors.DecodingError(cls, "Unterminated string")
        return result, value[1:]  # value contains "\x00" at its start
