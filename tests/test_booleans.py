"""
Tests for the `Boolean` datatype
"""
from cain.types import Boolean


def test_encode():
    """
    Tests the `Boolean` datatype encoding logic
    """
    b = Boolean(True)
    assert b.encoded == b'\x01'
    assert Boolean.encode(False) == b'\x00'


def test_decode():
    """
    Tests the `Boolean` datatype decoding logic
    """
    assert Boolean.decode(b'\x01') == True
    assert Boolean.decode(b'\x00') == False
