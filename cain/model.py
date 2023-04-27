"""
model.py

Defines the base classes for data models
"""

import typing

from cain import errors


class Datatype:
    """
    Holds a value and the different implementations to encode and
    decode between Python objects and Cain objects.
    """

    def __init__(self, value: typing.Any) -> None:
        self.value = value

    @classmethod
    def _encode(cls, value: typing.Any, *args) -> bytes:
        """
        The implementation of the encoding logic (Python -> Cain)

        Parameters
        ----------
        value: Any
            The data to encode
        *args: tuple[str, type]
            Any argument passed with the type.

        Returns
        -------
        bytes
            The encoded value
        """
        raise errors.EncodingError(cls, f"A value could not be encoded to `{cls.__name__}`")

    @classmethod
    def _decode(cls, value: bytes, *args) -> typing.Tuple[typing.Any, bytes]:
        """
        The implementation of the decoding logic (Cain -> Python)

        Parameters
        ----------
        value: bytes
            The data to decode (the data to decode is contained in the first few bytes)
        *args: tuple[str, type]
            Any argument passed with the type.

        Returns
        -------
        tuple[Any, bytes]
            The decoded value and the remaining bytes from `value` after decoding
        """
        raise errors.DecodingError(cls, f"A value could not be decoded to `{cls.__name__}` value")

    @classmethod
    def encode(cls, value: typing.Any, *args) -> bytes:
        """
        Encodes the given `value`

        Parameters
        ----------
        value: bytes
            The data to encode
        *args: tuple[str, type]
            Any argument passed with the type.

        Returns
        -------
        bytes
            The encoded value

        Raises
        ------
        EncodingError
            If the value could not be encoded
        """
        return cls._encode(value)

    @property
    def encoded(self) -> bytes:
        """
        The encoded value
        """
        return self.encode(self.value)

    @classmethod
    def decode(cls, value: bytes, *args) -> typing.Any:
        """
        Decodes the given `value`

        Parameters
        ----------
        value: bytes
            The data to decode
        *args: tuple[str, type]
            Any argument passed with the type.

        Returns
        -------
        Any
            The decoded value

        Raises
        ------
        DecodingError
            If the value could not be decoded
        """
        data, _ = cls._decode(value)
        return data

    @property
    def preview(self) -> str:
        """
        Returns a preview of the value

        Example
        -------
        >> > a = Datatype(b"Hello, this is a long byte string")
        >> > a.preview()
        'Hello...tring'
        """
        data = str(self)

        return "{}{}{}".format(
            data[:5],
            '.' * max(0, len(data) - 10),
            data[-5:]
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.preview})"

    def __str__(self) -> str:
        return str(self.value)
