"""
cain

A small yet powerful data format!
"""

import typing

from cain.model import Datatype
from cain.types import retrieve_type

Schema = typing.Union[typing.Type[Datatype], Datatype, type]


def dumps(obj: typing.Any, schema: Schema) -> bytes:
    """
    Encodes the given object `obj` as a Cain formatted data, following `schema`.

    Parameters
    ----------
    obj: typing.Any
        The object to encode.
    schema: type[Datatype] | Datatype | type
        The schema to use for the encoding.

    Returns
    -------
    bytes
        The encoded data.

    Examples
    --------
    >>> import cain
    >>> from cain.types import Object, Optional
    >>> dumps({"a": 2}, Object[{"a": int}])
    b'\x00\x00\x02'
    >>> class TestObject(Object):
    ...     bar: tuple[str, Optional[str], float, int]
    ...
    >>> cain.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}], list[str, TestObject])
    b'\x00foo\x00\x00\x00baz\x00\x00\x00\x00\x80?\x00\x02'
    >>> print(cain.dumps("\"foo\bar", str))
    b'"foo\x08ar\x00'
    >>> print(cain.dumps('\u1234', str))
    b'\xe1\x88\xb4\x00'
    >>> print(cain.dumps('\\', str))
    b'\\\x00'
    """
    encoder, type_args = retrieve_type(schema)
    return encoder.encode(obj, *type_args)


def dump(obj: typing.Any, handler: typing.BinaryIO, schema: Schema) -> None:
    """
    Encodes the given object `obj` as a Cain formatted data, following `schema`
    and writes it to the given file-like object `fp`.

    Parameters
    ----------
    obj: Any
        The object to encode.
    fp: BinaryIO
        The file-like object to write the encoded data to.
    schema: type[Datatype] | Datatype | type
        The schema to use for the encoding.

    Examples
    --------
    >>> import cain
    >>> from cain.types import Object, Optional
    >>> schema = list[str, Object[{"bar": tuple[str, Optional[str], float, int]}]]
    >>> with open('test.cain', 'w+b') as fp:
    ...     cain.dump(['foo', {'bar': ('baz', None, 1.0, 2)}], fp, schema)
    ...
    >>> with open('test.cain', 'r+b') as fp:
    ...     print(fp.read())
    ...
    b'\x00foo\x00\x00\x00baz\x00\x00\x00\x00\x80?\x00\x02'
    """
    handler.write(dumps(obj, schema))


def loads(obj: bytes, schema: Schema) -> typing.Any:
    """
    Decodes the given Cain formatted data `obj` following `schema`.

    Parameters
    ----------
    obj: bytes
        The Cain formatted data to decode.
    schema: type[Datatype] | Datatype | type
        The schema to use for the decoding.

    Returns
    -------
    typing.Any
        The decoded object.

    Examples
    --------
    >>> import cain
    >>> from cain.types import Optional, Object
    >>> schema = list[str, Object[{"bar": tuple[str, Optional[str], float, int]}]]
    >>> cain.loads(b'\x00foo\x00\x00\x00baz\x00\x00\x00\x00\x80?\x00\x02', schema)
    ['foo', {'bar': ('baz', None, 1.0, 2)}]
    >>> print(cain.loads(b'"foo\x08ar\x00', str))
    "foar
    >>> print(cain.loads(b'\xe1\x88\xb4\x00', str))
    ሴ
    >>> print(cain.loads(b'\\\x00', str))
    \
    """
    encoder, type_args = retrieve_type(schema)
    return encoder.decode(obj, *type_args)


def load(handler: typing.BinaryIO, schema: Schema) -> typing.Any:
    """
    Reads the Cain formatted data from `fp` and decodes it following `schema`.

    Parameters
    ----------
    fp: typing.Any
        The file-like object to read the Cain formatted data from.
    schema: type[Datatype] | Datatype | type
        The schema to use for the decoding.

    Returns
    -------
    typing.Any
        The decoded object.

    Examples
    --------
    >>> import cain
    >>> from cain.types import Optional, Object
    >>> schema = list[str, Object[{"bar": tuple[str, Optional[str], float, int]}]]
    >>> with open('test.cain', 'w+b') as fp:
    ...     cain.dump(['foo', {'bar': ('baz', None, 1.0, 2)}], fp, schema)
    ...
    >>> with open('test.cain', 'r+b') as fp:
    ...     cain.load(fp, schema)
    ...
    ['foo', {'bar': ('baz', None, 1.0, 2)}]
    """
    return loads(handler.read(), schema)
