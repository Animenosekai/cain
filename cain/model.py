"""
model.py

Defines the base classes for data models
"""

import typing
import copy

from cain import errors


class Datatype:
    """
    Holds a value and the different implementations to encode and
    decode between Python objects and Cain objects.
    """
    # Holds the different type arguments
    # Warning: Should only be modified in a copy of the class
    __args__ = []
    __annotations__ = {}

    def __init__(self, value: typing.Any) -> None:
        self.value = value

    # # When calling an already instantiated object, the __init__ method is called
    # # This happens when we are giving type arguments before using the class.
    # # Example: Datatype[int, str]("hello")
    # def __call__(self, value: typing.Any, *args) -> typing.Self:
    #     self.value = value
    #     return self

    def __class_getitem__(cls, args):
        """
        Called when using giving type arguments to the class.

        Parameters
        ----------
        cls: Datatype
            The actual class which is being instantiated
        args: str | type | dict | tuple[str | type | dict]
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

        annotations_r = {**cls.__annotations__}
        args_r = [*cls.__args__]

        for element in args:
            if isinstance(element, dict):
                annotations_r.update(element)
            else:
                args_r.append(element)

        class NewDatatype(cls):
            """A subclass containing the type arguments"""
            __annotations__ = annotations_r
            __args__ = args_r
        NewDatatype.__name__ = cls.__name__

        return NewDatatype

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
        value: Any
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
        return cls._encode(value, *(*cls.__args__, *args))

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
        data, _ = cls._decode(value, *(*cls.__args__, *args))
        return data

    def __repr__(self) -> str:
        """
        Returns a string representation of the object

        Returns
        -------
        str
            The string representation of the object.
            Example: "Datatype[int, str]('hello')"
                     "Datatype[int, str](42)"
                     "Datatype<{'a': int}>"
                     "Datatype<{'a': int}>({'a': 2})"
        """
        result = self.__class__.__name__
        if self.__annotations__:
            annotations_r = {}
            for key, value in self.__annotations__.items():
                try:
                    annotations_r[key] = value.__name__
                except AttributeError:
                    annotations_r[key] = str(value)
            result += f"<{annotations_r}>"
        if self.__args__:
            args_r = []
            for arg in self.__args__:
                try:
                    args_r.append(arg.__name__)
                except AttributeError:
                    args_r.append(str(arg))
            result += f"[{', '.join(args_r)}]"
        if self.value:
            result += f"({self.value})"
        return result

    def __str__(self) -> str:
        return str(self.value)
