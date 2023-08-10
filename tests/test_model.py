"""
Tests for custom datatypes and the base `Datatype` model
"""
import typing
from cain.model import Datatype


class MyObject(Datatype):
    @classmethod
    def _encode(cls, value: typing.Any, *args) -> bytes:
        return b'encoded data'

    @classmethod
    def _decode(cls, value: bytes, *args) -> typing.Tuple[typing.Any, bytes]:
        return 'decoded data', value


def test_custom():
    assert MyObject.encode('data') == b'encoded data'
    assert MyObject.decode(b'encoded data') == 'decoded data'
    assert MyObject("data").encoded == b'encoded data'
    assert typing.get_type_hints(MyObject[{"hey": int}]) == {"hey": int}
    assert typing.get_type_hints(MyObject[{"hey": int}, str]) == {"hey": int}
    assert MyObject[{"hey": int}, str].__args__ == [str]
    assert MyObject[{"hey": int}, str, int].__args__ == [str, int]
    assert MyObject[str, int].__args__ == [str, int]
