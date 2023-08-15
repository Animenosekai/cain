# Cain

<img align="right" src="./assets/cain.png" height="220px">

***A small yet powerful data format ✨***

<br>
<br>

[![PyPI version](https://badge.fury.io/py/cain.svg)](https://pypi.org/project/cain/)
[![Downloads](https://static.pepy.tech/personalized-badge/cain?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Total%20Downloads)](https://pepy.tech/project/cain)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/cain)](https://pypistats.org/packages/cain)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cain)](https://pypi.org/project/cain/)
[![PyPI - Status](https://img.shields.io/pypi/status/cain)](https://pypi.org/project/cain/)
[![GitHub - License](https://img.shields.io/github/license/Animenosekai/cain)](https://github.com/Animenosekai/cain/blob/master/LICENSE)
[![GitHub top language](https://img.shields.io/github/languages/top/Animenosekai/cain)](https://github.com/Animenosekai/cain)
[![CodeQL Checks Badge](https://github.com/Animenosekai/cain/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Animenosekai/cain/actions/workflows/codeql-analysis.yml)
![Code Size](https://img.shields.io/github/languages/code-size/Animenosekai/cain)
![Repo Size](https://img.shields.io/github/repo-size/Animenosekai/cain)
![Issues](https://img.shields.io/github/issues/Animenosekai/cain)

## Index

- [Index](#index)
- [Purpose](#purpose)
  - [Comparison](#comparison)
    - [JSON](#json)
    - [Cain](#cain-1)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
- [Installing](#installing)
  - [Option 1: From PyPI](#option-1-from-pypi)
  - [Option 2: From Git](#option-2-from-git)
- [Usage](#usage)
  - [Python](#python)
    - [Encoding](#encoding)
    - [Decoding](#decoding)
    - [Handling Schemas](#handling-schemas)
      - [Encoding](#encoding-1)
      - [Decoding](#decoding-1)
    - [Custom Encoder](#custom-encoder)
  - [CLI](#cli)
    - [Examples](#examples)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Authors](#authors)
- [Licensing](#licensing)

## Purpose

Cain is a new data interchange format which aims at providing the smallest possible size to encode data.

It is based on pre-defined schemas which leverages the need to specify it within the final encoded data.

> **Note**  
> Look at the [*SPECIFICATIONS*](https://github.com/Animenosekai/cain/blob/main/SPECIFICATIONS.md) file for more information on the purpose and idea behind this project.

### Comparison

For example, we consider the following object:

```python
{
    "b": 3,
    "c": 5.5,
    "d": True,
    "e": {
        "f": False,
        # "g": b"Hello world"
        "h": "HELLO WORLD",
        "i": "Hi!",
        "j": [1, 2, 3, 1, 1],
        "k": (1, "hello", True),
        "l": None,
        "m": "Yay",
        "n": "Hi",
        "o": 2,
        "p": None
    }
}
```

#### JSON

This is the expected result from a minified JSON encoding:

```json
{"b":3,"c":5.5,"d":true,"e":{"f":false,"h":"HELLO WORLD","i":"Hi!","j":[1,2,3,1,1],"k":[1,"hello",true],"l":null,"m":"Yay","n":"Hi","o":2,"p":null}}
```

#### Cain

This is the expected result from the Cain data format:

```cain
\x00\x00\x03\x00\x00\xb0@\x01\x00\x00HELLO WORLD\x00Hi!\x00\x00\x05\x00\x00\x00\x01\x00\x02\x00\x03\x00\x01\x00\x01\x00\x00\x01hello\x00\x01\x00\x01\x00Yay\x00\x00Hi\x00\x01\x00\x02
```

> **Note**  
> This is 56.76% smaller than the JSON version ✨

***Moreover, objects which can't be encoded using JSON (bytes, set, range, etc.) or wrongly encoded using JSON (ex: tuple) are working out of the box with Cain!***

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You will need Python 3 to use this module

```bash
# vermin output
Minimum required versions: 3.8
Incompatible versions:     2
```

Always check if your Python version works with `cain` before using it in production.

## Installing

### Option 1: From PyPI

```bash
pip install --upgrade cain
```

> This will install the latest version from PyPI

### Option 2: From Git

```bash
pip install --upgrade git+https://github.com/Animenosekai/cain.git
```

> This will install the latest development version from the git repository

You can check if you successfully installed it by printing out its version:

```bash
$ cain --version
1.1
```

## Usage

### Python

The main entry point ([cain.py](./cain/cain.py)) provides an API familiar to users of the standard library `json` module. The different datatype also present a very pythonic way of handling data to keep a nice and clean codebase.

#### Encoding

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
>>> from cain.types import Int
>>> from cain.types.numbers import unsigned
>>> Int[unsigned].encode(4)
b'\x00\x04'
```

You can also add a header using the `include_header` parameter to add a header containing the schema for the encoding data. This gives a more portable output but increases its size.

#### Decoding

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
>>> from cain.types import Int
>>> from cain.types.numbers import unsigned
>>> Int[unsigned].decode(b'\x00\x04')
4
```

#### Handling Schemas

If you want to dynamically encode/decode data with the Cain format, it is also possible to encode/decode the schema.

This is especially useful when developing a public API for example.

##### Encoding

```python
>>> import cain
>>> from cain.types import Object, Optional
>>> cain.encode_schema(Object[{"a": int}])
b'\x00\x00\x01\x00\x00a\x00\x00\x01\x00\x00\x01\x03\x00\x01\x02\x00\x00\x00\x00\x06\x00\x00\x00\x00\x16'
>>> class TestObject(Object):
...     bar: tuple[str, Optional[str], float, int]
...
>>> cain.encode_schema(list[str, TestObject])
b'\x01\x02\x00\x01\x00\x00\x00\x00\x00\x02\x00\x00...\x00\x16\x01\x00TestObject\x00\x00\x00'
```

##### Decoding

```python
>>> import cain
>>> cain.decode_schema(b'\x00\x00\x01\x00\x00a\x00\x00\x01\x00\x00\x01\x03\x00\x01\x02\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x16\x00')
Object<{'a': Int}>
>>> cain.decode_schema(b'\x01\x02\x00\x01\x00\x00\x00\x00\x00\x02\x00\x00...\x00\x16\x01\x00TestObject\x00\x00\x00')
Array[String, TestObject]
```

#### Custom Encoder

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

> **Warning**  
> Keep in mind that custom datatypes outside of subclasses of `Object` won't be able to be encoded by the Type encoder (used in schema headers for example)

### CLI

Cain has a pretty complete command-line interface, which lets you manipulate and interact with the Cain data format easily.

For more information, head over to your console and enter:

```bash
cain --help
```

Or

```bash
cain <action> --help
```

#### Examples

> Example usage of the CLI

Preparing the schema:

```python
# test.py
from cain import Object
class Test(Object):
    username: str
    favorite_number: int
```

Trying to encode with a Python schema:

```bash
cain encode '{"username": "Anise", "favorite_number": 2}' --schema="test.py" --schema-name="Test" --include-header --output="test.cain"
```

Trying to decode the previous file:

```bash
$ cain decode test.cain
{
    "favorite_number": 2,
    "username": "Anise"
}
```

Looking up at its schema:

```bash
$ cain schema lookup test.cain --schema-header
{
    "index": 22,
    "name": "Test",
    "annotations_keys": [
        "username",
        "favorite_number"
    ],
    "annotations_values": [
        {
            "index": 26,
            "name": null,
            "annotations_keys": [],
            "annotations_values": [],
            "arguments": [],
            "datatype": "String"
        },
        {
            "index": 6,
            "name": null,
            "annotations_keys": [],
            "annotations_values": [],
            "arguments": [],
            "datatype": "Int"
        }
    ],
    "arguments": [],
    "datatype": "Object"
}
```

Exporting its schema:

```bash
cain schema export test.cain --schema-header --output test.cainschema
```

Trying to encode another object with the exported schema:

```bash
$ cain encode '{"username": "yay", "favorite_number": 3}' --schema=test.cainschema
\x00\x00\x03yay\x00
```

Encoding "Hello world":

```bash
$ cain encode '"Hello world"' --schema="str" --schema-eval
Hello world\x00
$ cain encode '["Hello", "world"]' --schema="list[str]" --schema-eval
\x00\x02\x00\x00Hello\x00world\x00
```

## Deployment

This module is currently in development and might contain bugs.

This comes with a few disadvantages (for example, it takes a longer time to encode objects with Cain than with the standard `json` module) but this is expected to improve over time.

Please verify and test the module thoroughly before releasing anything at a production stage.

Feel free to report any issue you might encounter on Cain's GitHub page.

## Contributing

Pull requests are welcome. For major changes, please open a discussion first to discuss what you would like to change.

Please make sure to update the tests accordingly.

## Authors

- **Animenosekai** - *Initial work* - [Animenosekai](https://github.com/Animenosekai)

## Licensing

This software is licensed under the MIT License. See the [*LICENSE*](./LICENSE) file for more information.
