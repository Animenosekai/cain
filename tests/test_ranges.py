"""
Tests for the `Range` datatype
"""
from cain.types import Range


def test_encode():
    """
    Tests the `Optional` datatype encoding logic
    """
    r = Range(range(0, 4, 2))
    assert r.encoded == b'\x00\x04\x02'
    assert Range.encode(range(0, 4, 2)) == b'\x00\x04\x02'


def test_decode():
    """
    Tests the `Range` datatype decoding logic
    """
    assert Range.decode(b'\x00\x04\x02') == range(0, 4, 2)
