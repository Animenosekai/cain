"""
Tests for the `String` datatype
"""
from cain.types import String


def test_encode():
    """
    Tests the `String` datatype encoding logic
    """
    s = String("Hello world")
    assert s.encoded == b'Hello world\x00'
    assert String.encode("夏祭り") == b'\xe5\xa4\x8f\xe7\xa5\xad\xe3\x82\x8a\x00'


def test_decode():
    """
    Tests the `String` datatype decoding logic
    """
    assert String.decode(b'Hello world\x00') == "Hello world"
    assert String.decode(b'\xe5\xa4\x8f\xe7\xa5\xad\xe3\x82\x8a\x00') == '夏祭り'
