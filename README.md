# Cain

Cain is a new data interchange format which aims at providing the smallest possible size to encode data.

It is based on pre-defined schemas which leverages the need to specify it within the final encoded data.

## Index

- [Index](#index)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
- [Installing](#installing)
  - [Option 2: From Git](#option-2-from-git)
- [Usage](#usage)
- [Licensing](#licensing)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You will need Python 3 to use this module

```bash
# vermin output
Minimum required versions: 3.8
Incompatible versions:     2
```

Always check if your Python version works with `cain` before using it in production

## Installing

<!-- ### Option 1: From PyPI

```bash
pip install --upgrade cain
``` -->

### Option 2: From Git

```bash
pip install --upgrade git+https://github.com/Animenosekai/cain
```

You can check if you successfully installed it by printing out its version:

<!-- ```bash
$ cain --version
# output:
translatepy v2.3
```

or just: -->

```bash
$ python -c "import cain; print(cain.__version__)"
# output:
cain v2.3
```

## Usage

The main entry point ([cain.py](./cain/cain.py)) provides an API familiar to users of the standard library `json` module. The different datatypes also present a very pythonic way of handling data to keep a nice and clean codebase.

Encoding basic Python object hierarchies:

```python
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
```

Decoding Cain:

```python
>>> import cain
>>> from cain.types import Optional, Object
>>> schema = list[str, Object[{"bar": tuple[str, Optional[str], float, int]}]]
>>> cain.loads(b'\x00foo\x00\x00\x00baz\x00\x00\x00\x00\x80?\x00\x02', schema)
['foo', {'bar': ('baz', None, 1.0, 2)}]
>>> with open('test.cain', 'r+b') as fp:
...     cain.load(fp, schema)
...
['foo', {'bar': ('baz', None, 1.0, 2)}]
```

You can also create your own encoders:

```python
>>> import typing
>>> from cain.model import Datatype
>>> class MyObject(Datatype):
...     @classmethod         # *args contains the args passed here : MyObject[args]
...     def _encode(cls, value: typing.Any,*args) -> bytes:
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
```

## Licensing

This software is licensed under the MIT License. See the [*LICENSE*](./LICENSE) file for more information.
