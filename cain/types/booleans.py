"""
booleans


"""
from cain.model import Datatype
from cain import errors


class Boolean(Datatype):
    """
    Handles the encoding and decoding of booleans.
    """

    @classmethod
    def encode(cls, value: int, *args):
        return b'\x01' if value else b'\x00'

    @classmethod
    def decode(cls, value: bytes, *args):
        # could allow for booleans as integers or strings in `args`
        if value.startswith(b'\x00'):
            return False, value[1:]
        elif value.startswith(b'\x01'):
            return True, value[1:]
        raise errors.DecodingError(cls, "The given value does not seem to be a boolean")
