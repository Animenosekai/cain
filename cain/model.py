"""
model

Defines the base classes for data models
"""

import typing

from cain import errors


class DatatypeCache:
    """
    Holds the cache for a `Datatype` instance
    """

    def __init__(self) -> None:
        self.encoded: typing.Optional[bytes] = None
        # self.decoded: typing.Optional[typing.Any] = None

    def free(self):
        """
        Frees the cache
        """
        self.__init__()


class NullDatatypeCache(DatatypeCache):
    """
    Cache instance to avoid caching anything
    """

    def __setattribute__(self, key: str, value: typing.Any):
        return


class Datatype:
    """
    Holds a value and the different implementations to encode and
    decode between Python objects and Cain objects.
    """
    # CACHE_TYPE: typing.Optional[typing.Type[DatatypeCache]] = DatatypeCache

    def __init__(self, value: typing.Any) -> None:
        self.value = value
        self.cache = DatatypeCache()
        # self.cache = self.CACHE_TYPE() if self.CACHE_TYPE else NullDatatypeCache()

    @classmethod
    def encode(cls, value: typing.Any, *args) -> bytes:
        """
        The encoding logic (Python -> Cain)
        """
        raise errors.EncodingError(cls, f"A value could not be encoded to `{cls.__name__}`")

    @classmethod
    def decode(cls, value: bytes, *args) -> typing.Tuple[typing.Any, bytes]:
        """
        The decoding logic (Cain -> Python)

        Returns
        -------
        tuple[Any, bytes]
            The decoded value and the remaining bytes
        """
        raise errors.DecodingError(cls, f"A value could not be decoded to `{cls.__name__}` value")

    @classmethod
    def decoded(cls, value: bytes) -> typing.Any:
        """
        The decoded value
        """
        data, _ = cls.decode(value)
        return data

    @property
    def encoded(self) -> bytes:
        """
        The encoded value
        """
        if self.cache.encoded is None:
            data = self.encode(self.value)
            self.cache.encoded = data
        else:
            data = self.cache.encoded
        return data

    @property
    def preview(self) -> str:
        """
        Returns a preview of the value

        Example
        -------
        >>> a = Datatype(b"Hello, this is a long byte string")
        >>> a.preview()
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


class Reference:
    """
    A mutable reference to a data
    """

    def __init__(self, data: bytes) -> None:
        self.data = data
