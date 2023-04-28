"""
Tests for the `Number` datatype
"""
import decimal
from cain.types.numbers import (Number,
                                Float, Double, Decimal,
                                Complex, DoubleComplex,
                                Int, SignedInt,  UnsignedInt,
                                Int8, Int16, Int32, Int64,
                                UInt8, UInt16, UInt32, UInt64,
                                recommended_size,
                                long, short, signed, unsigned)


def test_encode():
    """
    Tests the `Number` datatype encoding logic
    """
    # Number
    n = Number(3.14)
    assert n.encoded == b'\x1f\x85\xebQ\xb8\x1e\t@'
    assert Number.encode(3.14) == b'\x1f\x85\xebQ\xb8\x1e\t@'

    # Floats
    assert Float.encode(3.14) == b'\xc3\xf5H@'
    assert Double.encode(3.14) == b'\x1f\x85\xebQ\xb8\x1e\t@'
    assert Decimal.encode(3.14) == b'3.14\x00'

    # Complex
    assert Complex(2+3j).encoded == b'\x00\x00\x00@\x00\x00@@'
    assert DoubleComplex(2+3j).encoded == b'\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x08@'

    # Integers
    assert Int.encode(3) == b'\x00\x03'
    assert Int.encode(3, "short") == b'\x03'
    assert Int.encode(3, "long") == b'\x00\x00\x03'
    assert Int["long"].encode(3) == b'\x00\x00\x03'
    assert Int[long].encode(3) == b'\x00\x00\x03'

    assert Int[long, short, unsigned].encode(3) == b'\x00\x03'
    assert Int[short, unsigned].encode(255) == b'\xff'
    assert UnsignedInt[short].encode(255) == b'\xff'

    assert Int[short, signed].encode(127) == b'\x7f'
    assert Int[short, signed].encode(-128) == b'\x80'
    assert SignedInt[short](127).encoded == b'\x7f'
    assert SignedInt[short](-128).encoded == b'\x80'

    assert UInt8.encode(255) == b'\xff'
    assert UInt16.encode(65_535) == b'\xff\xff'
    assert UInt32.encode(4_294_967_295) == b'\xff\xff\xff\xff'
    assert UInt64.encode(18_446_744_073_709_551_615) == b'\xff\xff\xff\xff\xff\xff\xff\xff'

    assert Int8.encode(127) == b'\x7f'
    assert Int16.encode(32_767) == b'\x7f\xff'
    assert Int32.encode(2_147_483_647) == b'\x7f\xff\xff\xff'
    assert Int64.encode(9_223_372_036_854_775_807) == b'\x7f\xff\xff\xff\xff\xff\xff\xff'


def test_decode():
    """
    Tests the `Number` datatype decoding logic
    """
    # Number
    assert Number.decode(b'\x1f\x85\xebQ\xb8\x1e\t@') == 3.14

    # Floats
    assert Float.decode(b'\xc3\xf5H@') - 3.14 < 1e4
    assert Double.decode(b'\x1f\x85\xebQ\xb8\x1e\t@') == 3.14
    assert Decimal.decode(b'3.14\x00') == decimal.Decimal('3.14')

    # Complex
    assert Complex.decode(b'\x00\x00\x00@\x00\x00@@') == 2+3j
    assert DoubleComplex.decode(b'\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x08@') == 2+3j

    # Integers
    assert Int.decode(b'\x00\x03') == 3
    assert Int.decode(b'\x03', "short") == 3
    assert Int.decode(b'\x00\x00\x03', "long") == 3

    assert Int["long"].decode(b'\x00\x00\x03') == 3
    assert Int[long].decode(b'\x00\x00\x03') == 3
    assert Int[long, short, unsigned].decode(b'\x00\x03') == 3

    assert Int[short, unsigned].decode(b'\xff') == 255
    assert Int[short, unsigned].decode(b'\xff') == 255
    assert UnsignedInt[short].decode(b'\xff') == 255

    assert Int[short, signed].decode(b'\x7f') == 127
    assert Int[short, signed].decode(b'\x80') == -128
    assert Int[short, signed].decode(b'\x80') == -128
    assert SignedInt[short].decode(b'\x7f') == 127
    assert SignedInt[short].decode(b'\x80') == -128

    assert UInt8.decode(b'\xff') == 255
    assert UInt16.decode(b'\xff\xff') == 65_535
    assert UInt32.decode(b'\xff\xff\xff\xff') == 4_294_967_295
    assert UInt64.decode(b'\xff\xff\xff\xff\xff\xff\xff\xff') == 18_446_744_073_709_551_615

    assert Int8.decode(b'\x7f') == 127
    assert Int16.decode(b'\x7f\xff') == 32_767
    assert Int32.decode(b'\x7f\xff\xff\xff') == 2_147_483_647
    assert Int64.decode(b'\x7f\xff\xff\xff\xff\xff\xff\xff') == 9_223_372_036_854_775_807


def test_recommended_size():
    """
    Tests the `recommended_size` function
    """
    assert recommended_size(2**8 - 1) == UInt8
    assert recommended_size(2**16 - 1) == UInt16
    assert recommended_size(2**32 - 1) == UInt32
    assert recommended_size(2**64 - 1) == UInt64

    assert recommended_size(-(2**8)//2) == Int8
    assert recommended_size(-(2**16)//2) == Int16
    assert recommended_size(-(2**32)//2) == Int32
    assert recommended_size(-(2**64)//2) == Int64
