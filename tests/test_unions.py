"""
Tests for the `Union` datatype
"""
from cain.types import Union
from cain.types.numbers import Int, short


def test_encode():
    """
    Tests the `Union` datatype encoding logic
    """
    assert Union.encode("Hello world", str) == b'Hello world\x00'
    assert Union.encode("Hello world", str, int) == b'\x00Hello world\x00'
    assert Union.encode(2, str, int) == b'\x01\x00\x02'
    assert Union.encode(2, str, Int[short]) == b'\x01\x02'


def test_decode():
    """
    Tests the `Union` datatype decoding logic
    """
    assert Union.decode(b'Hello world\x00', str) == 'Hello world'
    assert Union.decode(b'\x00Hello world\x00', str, int) == 'Hello world'
    assert Union.decode(b'\x01\x00\x02', str, int) == 2
    assert Union.decode(b'\x01\x02', str, Int[short]) == 2
    assert Union.decode(b'\x01\x02', str, Int[short], int) == 2
