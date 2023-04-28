"""
Tests for the `Array` datatype
"""
from cain.types import Array


def test_encode():
    """
    Tests the `Array` datatype encoding logic
    """
    assert Array[int]([1, 2, 3]).encoded == b'\x00\x03\x00\x00\x00\x01\x00\x02\x00\x03'
    assert Array[int].encode([1, 2, 3]) == b'\x00\x03\x00\x00\x00\x01\x00\x02\x00\x03'
    assert Array.encode([1, 2, 3], int) == b'\x00\x03\x00\x00\x00\x01\x00\x02\x00\x03'
    assert (Array.encode(["Hello", "Hi", "Hello", "Hey"], str)
            == b'\x00\x04\x00\x01\x00\x02\x00\x00\x00\x02Hello\x00Hi\x00Hey\x00')
    assert Array.encode(["Hello", 1], str, int) == b'\x00Hello\x00\x00\x01'
    assert Array[str, int, str].encode(["Hello", 1, "Yay"]) == b'\x00Hello\x00\x00\x01Yay\x00'
    assert Array[str, int].encode(["Hello", 1, "Yay"], str) == b'\x00Hello\x00\x00\x01Yay\x00'


def test_decode():
    """
    Tests the `Array` datatype decoding logic
    """
    assert Array[int].decode(b'\x00\x03\x00\x00\x00\x01\x00\x02\x00\x03') == [1, 2, 3]
    assert Array.decode(b'\x00\x03\x00\x00\x00\x01\x00\x02\x00\x03', int) == [1, 2, 3]
    assert (Array.decode(b'\x00\x04\x00\x01\x00\x02\x00\x00\x00\x02Hello\x00Hi\x00Hey\x00', str)
            == ["Hello", "Hi", "Hello", "Hey"])
    assert Array.decode(b'\x00Hello\x00\x00\x01', str, int) == ["Hello", 1]
    assert Array[str, int, str].decode(b'\x00Hello\x00\x00\x01Yay\x00') == ["Hello", 1, "Yay"]
    assert Array[str, int].decode(b'\x00Hello\x00\x00\x01Yay\x00', str) == ["Hello", 1, "Yay"]


def test_repetitions():
    """
    Tests the `Array` datatype data repetitions removal logic
    """
    # 1 integer for the number of indices, 2 for the indices

    # 3 new 2 bytes integers
    assert (len(Array[str].encode(["Hello", "Hi", "Hello", "Hey"]))
            == len(Array[str].encode(["Hello", "Hi", "Hey"])) + (3 * 2))
    # 1 new 2 bytes integers
    assert (len(Array[str].encode(["Hello", "Hi", "Hello", "Hey", "Hello"]))
            == len(Array[str].encode(["Hello", "Hi", "Hello", "Hey"])) + (1 * 2))

    # 1 integer for the new index

    # 3 new 2 bytes integers
    assert (len(Array[str, str, str, str].encode(["Hello", "Hi", "Hello", "Hey"]))
            == len(Array[str, str, str].encode(["Hello", "Hi", "Hey"])) + (3 * 1))
    # 1 new 2 bytes integers
    assert (len(Array[str, str, str, str, str].encode(["Hello", "Hi", "Hello", "Hey", "Hello"]))
            == len(Array[str, str, str, str].encode(["Hello", "Hi", "Hello", "Hey"])) + (1 * 1))
