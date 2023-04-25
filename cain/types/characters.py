"""
characters.py

Defines the Character datatype
"""
import typing
from cain.model import Datatype
from cain import errors

fixed_case = FIXED_CASE = FixedCase = "fixed_case"
ascii = ASCII = Ascii = "ascii"
unicode = UNICODE = Unicode = "unicode"

lower_case = LOWER_CASE = LowerCase = "lower_case"
upper_case = UPPER_CASE = UpperCase = "upper_case"

T = typing.TypeVarTuple("T")
FIXED_CASE_ALPHABET = ("NULL", *"ABCDEFGHIJKLMNOPQRSTUVWXYZ", *" \n\t")


class Character(Datatype, typing.Generic[*T]):
    """
    Handles the encoding and decoding of binary blob.
    """

    @staticmethod
    def process_char_range(args):
        """
        Returns the right character range
        """
        # print(args)
        # print(FIXED_CASE in args)
        char_range = UNICODE  # by default
        for arg in args:
            if isinstance(arg, typing.ForwardRef):
                arg = arg.__forward_arg__
            if arg in (FIXED_CASE, ASCII, UNICODE):
                char_range = arg
        return char_range

    @staticmethod
    def process_case(args):
        """
        Returns the right case
        """
        case_value = lower_case  # by default
        for arg in args:
            if isinstance(arg, typing.ForwardRef):
                arg = arg.__forward_arg__
            if arg in (LOWER_CASE, UPPER_CASE):
                case_value = arg
        return case_value

    @classmethod
    def encode(cls, value: str, *args):
        # length of blob + blob
        value = value[0]
        char_range = cls.process_char_range(args)
        if char_range == FIXED_CASE:
            value = value.upper()
            try:
                return FIXED_CASE_ALPHABET.index(value).to_bytes()  # TODO: should turn into a series of bits instead of creating a whole byte
            except ValueError as exc:
                raise errors.EncodingError(cls, f"The FixedCase encoding could not encode the character: `{value}`") from exc
        elif char_range == ASCII:
            return value.encode("ascii")
        else:
            return value.encode("utf-8")

    @classmethod
    def decode(cls, value: bytes, *args):
        char_range = cls.process_char_range(args)
        if char_range == FIXED_CASE:
            index = int.from_bytes(value[:1])
            case_value = cls.process_case(args)
            char = FIXED_CASE_ALPHABET[index]
            if case_value == LOWER_CASE:
                return char.lower(), value[1:]
            return char.upper(), value[1:]
        elif char_range == ASCII:
            return value[:1].decode("ascii"), value[1:]
        else:
            # TODO: Read Unicode specs
            return value[:1].decode("utf-8"), value[1:]