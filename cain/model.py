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

    def __init__(self, value: typing.Any, *args) -> None:
        self.value = value
        self.args = list(args)

    # When calling an already instantiated object, the __init__ method is called
    # This happens when we are giving type arguments before using the class.
    # Example: Datatype[int, str]("hello")
    def __call__(self, value: typing.Any, *args) -> typing.Self:
        self.value = value
        self.args.extend(args)
        return self

    def __class_getitem__(cls, args):
        """
        Called when using giving type arguments to the class.

        Parameters
        ----------
        cls: Datatype
            The actual class which is being instantiated
        args: tuple[str, type]
            The arguments passed with the type

        Example
        -------
        >>> from cain.model import Datatype
        >>> Datatype[int, str]("hello")
        Datatype[int, str]('hello')

        Returns
        -------
        Datatype
            The instantiated class
        """
        if not isinstance(args, tuple):
            args = (args,)
        return cls(None, *args)

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
        return cls._encode(value, *args)

    @property
    def encoded(self) -> bytes:
        """
        The encoded value
        """
        return self.encode(self.value, *self.args)

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
        data, _ = cls._decode(value, *args)
        return data

    def __repr__(self) -> str:
        if self.args:
            args = []
            for arg in self.args:
                try:
                    args.append(arg.__name__)
                except AttributeError:
                    args.append(str(arg))
            return f"{self.__class__.__name__}[{', '.join(args)}]({self.value})"
        return f"{self.__class__.__name__}({self.value})"

    def __str__(self) -> str:
        return str(self.value)
