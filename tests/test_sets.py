"""
Tests for the `Set` datatype
"""
from cain.types import Set, Union


def test_encode():
    """
    Tests the `Set` datatype encoding logic
    """
    assert Set[int]({1, 2, 3}).encoded == b'\x00\x03\x00\x00\x00\x01\x00\x02\x00\x03'
    assert Set[int].encode({1, 2, 3}) == b'\x00\x03\x00\x00\x00\x01\x00\x02\x00\x03'
    assert Set.encode({1, 2, 3}, int) == b'\x00\x03\x00\x00\x00\x01\x00\x02\x00\x03'


def test_decode():
    """
    Tests the `Set` datatype decoding logic
    """
    assert Set[int].decode(b'\x00\x03\x00\x00\x00\x01\x00\x02\x00\x03') == {1, 2, 3}
    assert Set.decode(b'\x00\x03\x00\x00\x00\x01\x00\x02\x00\x03', int) == {1, 2, 3}


def test_repetitions():
    """
    Tests the `Set` datatype data repetitions removal logic
    """
    # need to come up with tests for non equal values which are encoded equally

    # 1 integer for the number of indices, 2 for the indices

    # 1 integer for the new index
