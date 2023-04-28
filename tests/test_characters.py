"""
Tests for the `Character` datatype
"""
from cain.types import Character


def test_encode():
    """
    Tests the `Character` datatype encoding logic
    """
    c = Character("a")
    assert c.encoded == b"a"
    assert Character.encode("夏") == b'\xe5\xa4\x8f'


def test_decode():
    """
    Tests the `Character` datatype decoding logic
    """
    assert Character.decode(b"a") == 'a'
    assert Character.decode(b'\xe5\xa4\x8f') == '夏'
