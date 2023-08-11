"""
Cain <https://github.com/Animenosekai/cain> is a new data interchange
format which aims at providing the smallest possible size to encode data.

It is based on pre-defined schemas which leverages the need to specify it
within the final encoded data.

The main entry point (cain.py) provides an API familiar to users of the
standard library `json` module. The different datatypes also present
a very pythonic way of handling data to keep a nice and clean codebase.

Encoding basic Python object hierarchies:

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
>>> schema = list[str, Object[{"bar": tuple[str, Optional[str], float, int]}]]
>>> with open('test.cain', 'w+b') as fp:
...     cain.dump(['foo', {'bar': ('baz', None, 1.0, 2)}], fp, schema)
...
>>> from cain.types import Int
>>> from cain.types.numbers import unsigned
>>> Int[unsigned].encode(4)
b'\x00\x04'

Decoding Cain:

>>> import cain
>>> from cain.types import Optional, Object
>>> schema = list[str, Object[{"bar": tuple[str, Optional[str], float, int]}]]
>>> cain.loads(b'\x00foo\x00\x00\x00baz\x00\x00\x00\x00\x80?\x00\x02', schema)
['foo', {'bar': ('baz', None, 1.0, 2)}]
>>> with open('test.cain', 'r+b') as fp:
...     cain.load(fp, schema)
...
['foo', {'bar': ('baz', None, 1.0, 2)}]
>>> from cain.types import Int
>>> from cain.types.numbers import unsigned
>>> Int[unsigned].decode(b'\x00\x04')
4

You can also create your own encoders:

>>> import typing
>>> from cain.model import Datatype
>>> class MyObject(Datatype):
...     @classmethod         # *args contains the args passed here : MyObject[args]
...     def _encode(cls, value: typing.Any, *args) -> bytes:
...         ... #  your custom encoding
...         return b'encoded data'
...     #
...     @classmethod
...     def _decode(cls, value: bytes, *args) -> typing.Tuple[typing.Any, bytes]:
...         ... #  `value` contains more than just the value you should decode
...         ... #  try to only decode the first few bytes
...         ... #  your custom decoding
...         return 'decoded data', value # the rest of the value that you didn't decode
... # you can now use `MyObject` in your schemas and encode/decode from it

Licensing
---------
MIT License

Copyright (c) 2023 Animenosekai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__all__ = [
    # Modules
    'errors',
    'types',
    'model',

    # Classes
    'Datatype',
    'Object',
    'Type',

    # Functions
    'loads',
    'load',
    'dump',
    'dumps',
    'encode_schema',
    'decode_schema',

    # Versioning and copyrights
    "__author__",
    "__copyright__",
    "__license__",
    "__version__"
]

from . import errors, model, types
from .__info__ import __author__, __copyright__, __license__, __version__
from .cain import decode_schema, dump, dumps, encode_schema, load, loads, Type
from .model import Datatype
from .types import Object
