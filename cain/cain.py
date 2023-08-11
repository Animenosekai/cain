"""
cain

A small yet powerful data format!
"""

import typing

import cain.types
from cain.model import Datatype
from cain.types import retrieve_type
from cain.types.types import Type

# the Schema type
T = typing.TypeVar("T")
Schema = typing.Union[typing.Type[Datatype], Datatype, typing.Type[T]]


def dumps(obj: typing.Any,
          schema: Schema,
          include_header: typing.Union[bool, Type] = False) -> bytes:
    """
    Encodes the given object `obj` as a Cain formatted data, following `schema`.

    Parameters
    ----------
    obj: typing.Any
        The object to encode
    schema: type[Datatype] | Datatype | type
        The schema to use for the encoding
    include_header: bool, default = False
        This prepends a header containing the schema at the beginning of the content.
        Warning: This will significantly increase the size of the result (especially for
        originally small content)

    Returns
    -------
    bytes
        The encoded data.

    Examples
    --------
    >>> import cain
    >>> from cain.types import Object, Optional
    >>> cain.dumps({"a": 2}, Object[{"a": int}])
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
    value = encoder.encode(obj, *type_args)
    if include_header:
        header = encode_schema(schema)
        # I wondered if we should include some kind of version to the header
        # but I concluded that this should be up to the user choice to
        # increase the content size
        value = cain.types.Tuple[bytes, bytes].encode((header, value))
    return value


def dump(obj: typing.Any,
         handler: typing.BinaryIO,
         schema: Schema,
         include_header: bool = False) -> None:
    """
    Encodes the given object `obj` as a Cain formatted data, following `schema`
    and writes it to the given file-like object `fp`.

    Parameters
    ----------
    obj: Any
        The object to encode
    fp: BinaryIO
        The file-like object to write the encoded data to
    schema: type[Datatype] | Datatype | type
        The schema to use for the encoding
    include_header: bool, default = False
        This prepends a header containing the schema at the beginning of the content.
        Warning: This will significantly increase the size of the result (especially for
        originally small content)

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
    handler.write(dumps(obj, schema, include_header))


def loads(obj: bytes, schema: typing.Optional[Schema[T]] = None) -> T:
    """
    Decodes the given Cain formatted data `obj` following `schema`.

    Note: 

    Parameters
    ----------
    obj: bytes
        The Cain formatted data to decode.
    schema: type[Datatype] | Datatype | type | None, default = None
        The schema to use for the decoding.
        When left empty, the given `obj` should contain a header with the schema to decode it.

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
    if not schema:
        schema, obj = cain.types.Tuple[bytes, bytes].decode(obj)
        schema = Type.decode(schema)
    encoder, type_args = retrieve_type(schema)
    return encoder.decode(obj, *type_args)


def load(handler: typing.BinaryIO, schema: typing.Optional[Schema[T]] = None) -> T:
    """
    Reads the Cain formatted data from `fp` and decodes it following `schema`.

    Parameters
    ----------
    fp: typing.Any
        The file-like object to read the Cain formatted data from.
    schema: type[Datatype] | Datatype | type | None, default = None
        The schema to use for the decoding.
        When left empty, the given file should contain a header with the schema to decode it.

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


def encode_schema(schema: Schema) -> bytes:
    """
    Encodes the given schema as a Cain formatted data, to dynamically encode data

    Parameters
    ----------
    schema: type[Datatype] | Datatype | type
        The schema to encode

    Returns
    -------
    bytes
        The encoded schema

    Examples
    --------
    >>> import cain
    >>> from cain.types import Object, Optional
    >>> cain.encode_schema(Object[{"a": int}])
    b'\x00\x00\x01\x00\x00a\x00\x00\x01\x00\x00\x01\x03\x00\x01\x02\x00\x00\x00\x00\x06\x00\x00\x00\x00\x16'
    >>> class TestObject(Object):
    ...     bar: tuple[str, Optional[str], float, int]
    ...
    >>> cain.encode_schema(list[str, TestObject])
    b'\x01\x02\x00\x01\x00\x00\x00\x00\x00\x02\x00\x00...\x00\x16\x01\x00TestObject\x00\x00\x00'
    """
    return Type.encode(schema)


def decode_schema(schema: bytes) -> typing.Type[Datatype]:
    """
    Encodes the given schema as a Cain formatted data, to dynamically decode data

    Parameters
    ----------
    schema: bytes
        The schema to decode

    Returns
    -------
    type[Datatype]
        The datatype

    Examples
    --------
    >>> import cain
    >>> cain.decode_schema(b'\x00\x00\x01\x00\x00a\x00\x00\x01\x00\x00\x01\x03\x00\x01\x02\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x16\x00')
    Object<{'a': Int}>
    >>> cain.decode_schema(b'\x01\x02\x00\x01\x00\x00\x00\x00\x00\x02\x00\x00...\x00\x16\x01\x00TestObject\x00\x00\x00')
    Array[String, TestObject]
    """
    return Type.decode(schema)
