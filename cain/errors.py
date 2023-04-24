"""
errors

Defines the different errors which can be encountered while using the formatter
"""


class CainError(Exception):
    """
    The base for all of the errors which can be encountered using Cain
    """


class EncoderError(CainError):
    """
    Defines the errors which can happen at the encoder level
    """


class DatatypeError(EncoderError):
    """
    Defines the errors which can happen while handling data conversions (encoding or decoding from a format to another)
    """

    def __init__(self, datatype: type, *args) -> None:
        self.datatype = datatype
        super().__init__(*args)


class UnknownTypeError(DatatypeError):
    """
    Defines an error which could occur if passing an unknown type
    """


class EncodingError(DatatypeError):
    """
    Defines an error which could happen while encoding data (Python -> Cain)
    """


class DecodingError(DatatypeError):
    """
    Defines an error which could happen while decoding data (Cain -> Python)
    """
