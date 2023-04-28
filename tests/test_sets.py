"""
Tests for the `Set` datatype
"""
from cain.types import Set


def test_encode():
    """
    Tests the `Set` datatype encoding logic
    """
    assert Set[int].decode(Set[int]({1, 2, 3}).encoded) == {1, 2, 3}
    assert Set[int].decode(Set[int].encode({1, 2, 3})) == {1, 2, 3}
    assert Set.decode(Set.encode({1, 2, 3}, int), int) == {1, 2, 3}
    assert (Set.decode(Set.encode({"Hello", "Hi", "Hello", "Hey"}, str), str)
            == {"Hello", "Hi", "Hey"})
    assert Set.decode(Set.encode({"Hello", 1}, str, int), str, int) == {"Hello", 1}
    assert Set[str, int].decode(Set[str, int].encode({"Hello", 1})) == {"Hello", 1}


def test_decode():
    """
    Tests the `Set` datatype decoding logic
    """
    assert Set[int].decode(b'\x00\x03\x00\x00\x00\x01\x00\x02\x00\x03') == {1, 2, 3}
    assert Set.decode(b'\x00\x03\x00\x00\x00\x01\x00\x02\x00\x03', int) == {1, 2, 3}
    assert Set.decode(b'\x00\x03\x00\x00Hello\x00Hi\x00Hey\x00', str) == {"Hello", "Hi", "Hey"}
    assert Set.decode(b'\x00\x02\x00\x00\x00Hello\x00\x01\x00\x01', str, int) == {"Hello", 1}
    assert Set[str, int].decode(b'\x00\x02\x00\x00\x00Hello\x00\x01\x00\x01') == {"Hello", 1}


def test_repetitions():
    """
    Tests the `Set` datatype data repetitions removal logic
    """
    # need to come up with tests for non equal values which are encoded equally

    # 1 integer for the number of indices, 2 for the indices

    # 1 integer for the new index
