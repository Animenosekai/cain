"""
Tests for the `Optional` datatype
"""
from cain.types import Optional


def test_encode():
    """
    Tests the `Optional` datatype encoding logic
    """
    assert Optional.encode("Hello world", str) == b'\x01Hello world\x00'
    assert Optional.encode(None, str) == b"\x00"


def test_decode():
    """
    Tests the `Optional` datatype decoding logic
    """
    assert Optional.decode(b'\x01Hello world\x00', str) == 'Hello world'
    assert Optional.decode(b'\x00', str) is None
