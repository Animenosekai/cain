"""
Tests for the `Binary` datatype
"""
from cain.types import Binary


def test_encode():
    """
    Tests the `Binary` datatype encoding logic
    """
    b = Binary(b"Hello world")
    assert b.encoded == b'\x00\x00\x00\x0bHello world'
    assert Binary.encode(b"Hello world", "long") == b'\x00\x00\x00\x00\x0bHello world'


def test_decode():
    """
    Tests the `Binary` datatype decoding logic
    """
    assert Binary.decode(b"\x00\x00\x00\x0bHello world") == b"Hello world"
    assert Binary.decode(b"\x00\x00\x00\x00\x0bHello world", "long") == b"Hello world"
