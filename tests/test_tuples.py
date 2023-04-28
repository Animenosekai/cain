"""
Tests for the `Tuple` datatype
"""
from cain.types import Tuple


def test_encode():
    """
    Tests the `Tuple` datatype encoding logic
    """
    assert Tuple[int]((1, 2, 3)).encoded == b'\x00\x03\x00\x00\x00\x01\x00\x02\x00\x03'
    assert Tuple[int].encode((1, 2, 3)) == b'\x00\x03\x00\x00\x00\x01\x00\x02\x00\x03'
    assert Tuple.encode((1, 2, 3), int) == b'\x00\x03\x00\x00\x00\x01\x00\x02\x00\x03'
    assert (Tuple.encode(("Hello", "Hi", "Hello", "Hey"), str)
            == b'\x00\x04\x00\x01\x00\x02\x00\x00\x00\x02Hello\x00Hi\x00Hey\x00')
    assert Tuple.encode(("Hello", 1), str, int) == b'\x00Hello\x00\x00\x01'
    assert Tuple[str, int, str].encode(("Hello", 1, "Yay")) == b'\x00Hello\x00\x00\x01Yay\x00'
    assert Tuple[str, int].encode(("Hello", 1, "Yay"), str) == b'\x00Hello\x00\x00\x01Yay\x00'


def test_decode():
    """
    Tests the `Tuple` datatype decoding logic
    """
    assert Tuple[int].decode(b'\x00\x03\x00\x00\x00\x01\x00\x02\x00\x03') == (1, 2, 3)
    assert Tuple.decode(b'\x00\x03\x00\x00\x00\x01\x00\x02\x00\x03', int) == (1, 2, 3)
    assert (Tuple.decode(b'\x00\x04\x00\x01\x00\x02\x00\x00\x00\x02Hello\x00Hi\x00Hey\x00', str)
            == ("Hello", "Hi", "Hello", "Hey"))
    assert Tuple.decode(b'\x00Hello\x00\x00\x01', str, int) == ("Hello", 1)
    assert Tuple[str, int, str].decode(b'\x00Hello\x00\x00\x01Yay\x00') == ("Hello", 1, "Yay")
    assert Tuple[str, int].decode(b'\x00Hello\x00\x00\x01Yay\x00', str) == ("Hello", 1, "Yay")


def test_repetitions():
    """
    Tests the `Tuple` datatype data repetitions removal logic
    """
    # 1 integer for the number of indices, 2 for the indices

    # 3 new 2 bytes integers
    assert (len(Tuple[str].encode(("Hello", "Hi", "Hello", "Hey")))
            == len(Tuple[str].encode(["Hello", "Hi", "Hey"])) + (3 * 2))
    # 1 new 2 bytes integers
    assert (len(Tuple[str].encode(["Hello", "Hi", "Hello", "Hey", "Hello"]))
            == len(Tuple[str].encode(("Hello", "Hi", "Hello", "Hey"))) + (1 * 2))

    # 1 integer for the new index

    # 3 new 2 bytes integers
    assert (len(Tuple[str, str, str, str].encode(("Hello", "Hi", "Hello", "Hey")))
            == len(Tuple[str, str, str].encode(["Hello", "Hi", "Hey"])) + (3 * 1))
    # 1 new 2 bytes integers
    assert (len(Tuple[str, str, str, str, str].encode(["Hello", "Hi", "Hello", "Hey", "Hello"]))
            == len(Tuple[str, str, str, str].encode(("Hello", "Hi", "Hello", "Hey"))) + (1 * 1))
