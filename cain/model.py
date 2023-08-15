"""
model.py

Defines the base classes for data models
"""

import typing

from cain import errors


class DatatypeMeta(type):
    """A metaclass to give a better python representation of Datatypes,
    especially when dynamically sub-classing them"""

    def __repr__(cls) -> str:
        try:
            return cls().__repr__()
        except Exception:
            try:
                return str(cls)
            except Exception:
                try:
                    return cls.__name__
                except Exception:
                    return "Datatype(N/A)"

    @property
    def __type_hints__(cls):
        """Parses the type annotations for this class"""
        try:
            annotations, results = cls.__type_hints_cache__
            if annotations != cls.__annotations__:
                raise AttributeError("internal error: the annotations have changed")
            return results
        except AttributeError:
            # print("__type_hints__: cache miss")
            results = typing.get_type_hints(cls)
            cls.__type_hints_cache__ = (cls.__annotations__, results)
            return results

    def __eq__(cls, value: "DatatypeMeta") -> bool:
        if hasattr(cls, "__name__") or hasattr(value, "__name__"):
            try:
                name = cls.__name__ == value.__name__
            except AttributeError:
                name = False
        else:
            name = True

        try:
            value_type_hints = value.__type_hints__
        except AttributeError:
            try:
                value_type_hints = typing.get_type_hints(value)
            except Exception:
                value_type_hints = {}

        if hasattr(cls, "__args__") or hasattr(value, "__args__"):
            try:
                args = cls.__args__ == value.__args__
            except AttributeError:
                args = False
        else:
            args = True

        return (name
                and cls.__type_hints__ == value_type_hints
                and args)

    def __hash__(cls) -> int:
        return super().__hash__()


class Datatype(metaclass=DatatypeMeta):
    """
    Holds a value and the different implementations to encode and
    decode between Python objects and Cain objects.
    """
    # Holds the different type arguments
    # Warning: Should only be modified in a copy of the class
    __args__ = []
    __annotations__ = {}

    def __init__(self, value: typing.Any = None) -> None:
        self._cain_value = value

    # # When calling an already instantiated object, the __init__ method is called
    # # This happens when we are giving type arguments before using the class.
    # # Example: Datatype[int, str]("hello")
    # def __call__(self, value: typing.Any, *args) -> typing.Self:
    #     self._cain_value = value
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
    @property
    def __root__(cls):
        """Returns a version of the current datatype without any arguments or type annotations"""
        class NewDatatype(cls):
            """A subclass which doesn't have any type argument"""
            __annotations__ = {}
            __args__ = []
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
        raise errors.DecodingError(cls, f"A value could not be decoded to `{cls.__name__}`")

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
        return self.encode(self._cain_value)

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
            # annotations_r = {}
            # for key, value in typing.get_type_hints(self).items():
            #     try:
            #         annotations_r[key] = value.__name__
            #     except AttributeError:
            #         annotations_r[key] = str(value)
            try:
                result += f"<{self.__class__.__type_hints__}>"
            except Exception:
                result += f"<{self.__annotations__}>"
        if self.__args__:
            args_r = []
            for arg in self.__args__:
                try:
                    args_r.append(arg.__name__)
                except AttributeError:
                    args_r.append(str(arg))
            result += f"[{', '.join(args_r)}]"
        if self._cain_value:
            result += f"({self._cain_value})"
        return result

    def __str__(self) -> str:
        return str(self._cain_value)

    def __getattr__(self, key: str):
        if key == "_cain_value":
            return super().__getattribute__("_cain_value")
        return getattr(self._cain_value, key)

    def __getitem__(self, key: str):
        return self._cain_value[key]
