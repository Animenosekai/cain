"""
characters.py

Defines the Character datatype, which is used to store characters/letters.

Note: `Character` now only uses UTF-8 to encode its characters.

Note: It used to have other encodings, but they were removed because Python does not\
      support single bit manipulations very well.

Example
-------
>>> from cain.types import Character
>>> c = Character("a")
>>> c.encoded
b'a'
>>> Character.encode("夏")
b'\xe5\xa4\x8f'
>>> Character.decode(b'\xe5\xa4\x8f')
'夏'

Structure
---------
From: https://en.wikipedia.org/wiki/UTF-8#Encoding

Chararacter length  |        UTF-8 octet sequence
--------------------+----------------------------------------
1 byte character    | 0xxxxxxx
2 bytes character   | 110xxxxx 10xxxxxx
3 bytes character   | 1110xxxx 10xxxxxx 10xxxxxx
4 bytes character   | 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx

The `x` has the actual code point.
"""

from cain.model import Datatype


class Character(Datatype):
    """
    Handles the encoding and decoding of binary blob.

    Example
    -------
    >>> c = Character("a")
    >>> c.encoded
    b'a'
    >>> Character.encode("夏")
    b'\xe5\xa4\x8f'
    >>> Character.decode(b'\xe5\xa4\x8f')
    '夏'
    """

    @classmethod
    def _encode(cls, value: str, *args):
        return value[0].encode("utf-8")

    @classmethod
    def _decode(cls, value: bytes, *args):
        for i in range(1, 5):
            try:
                return value[:i].decode("utf-8"), value[i:]
            except UnicodeDecodeError:
                continue

        # In theory, it should never come here
        # Falling back to manual decoding
        # Removing 3 bits at the right of the byte, then checking if it starts with four `1`.
        if value[0] >> 3 == 0b11110:
            bytes_length = 4
        elif value[0] >> 4 == 0b1110:
            bytes_length = 3
        elif value[0] >> 5 == 0b110:
            bytes_length = 2
        else:
            bytes_length = 1
        # I don't actually understand why Unicode is using all of those extra `0`
        # before giving the codepoints and `10` at the start of each byte.
        # At least, we might be able to optimize to fit more characters, but it would require making
        # another standard.
        return value[:bytes_length].decode("utf-8"), value[bytes_length:]
