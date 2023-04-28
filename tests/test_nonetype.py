"""
Tests for the `NoneType` datatype
"""
from cain.types import NoneType


def test_encode():
    """
    Tests the `NoneType` datatype encoding logic
    """
    n = NoneType(None)
    assert n.encoded == b''
    assert NoneType.encode(None) == b''


def test_decode():
    """
    Tests the `NoneType` datatype decoding logic
    """
    assert NoneType.decode(b'') is None
