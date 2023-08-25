import cain
from cain.types import Optional, Object
from pathlib import Path
import typing

def test_dumps():
    assert cain.dumps({"a": 2}, Object[{"a": int}]) == b'\x00\x00\x02'

    class TestObject(Object):
        bar: typing.Tuple[str, Optional[str], float, int]

    assert (cain.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}], list[str, TestObject])
            == b'\x00foo\x00\x00\x00baz\x00\x00\x00\x00\x80?\x00\x02')

    assert cain.dumps("\"foo\bar", str) == b'"foo\x08ar\x00'
    assert cain.dumps('\u1234', str) == b'\xe1\x88\xb4\x00'
    assert cain.dumps('\\', str) == b'\\\x00'


def test_dump():
    schema = list[str, Object[{"bar": typing.Tuple[str, Optional[str], float, int]}]]
    with open('test.cain', 'w+b') as fp:
        cain.dump(['foo', {'bar': ('baz', None, 1.0, 2)}], fp, schema)

    # Cleanup
    Path("test.cain").unlink()


def test_loads():
    schema = list[str, Object[{"bar": typing.Tuple[str, Optional[str], float, int]}]]
    loaded = cain.loads(b'\x00foo\x00\x00\x00baz\x00\x00\x00\x00\x80?\x00\x02', schema)
    assert loaded[0] == "foo"
    assert loaded[1]._cain_value == {'bar': ('baz', None, 1.0, 2)}


def test_load():
    schema = list[str, Object[{"bar": typing.Tuple[str, Optional[str], float, int]}]]
    with open('test.cain', 'w+b') as fp:
        cain.dump(['foo', {'bar': ('baz', None, 1.0, 2)}], fp, schema)

    with open('test.cain', 'r+b') as fp:
        loaded = cain.load(fp, schema)
        assert loaded[0] == "foo"
        assert loaded[1]._cain_value == {'bar': ('baz', None, 1.0, 2)}

    # Cleanup
    Path("test.cain").unlink()
