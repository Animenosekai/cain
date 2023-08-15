"""
union.py

Defines the Union datatype, which is used to store values of variable types.

Example
-------
>>> from cain.types import Union
>>> Union.encode("Hello world", str)
b'Hello world\x00'
>>> Union.encode("Hello world", str, int)
b'\x00Hello world\x00'
>>> Union.encode(2, str, int)
b'\x01\x00\x02'
>>> from cain.types.numbers import Int, short
>>> Union.encode(2, str, Int[short])
b'\x01\x02'

Structure
---------
If there is only one type argument specified,
this argument will be used to encode and decode the value.

If there are multiple types possible for the value,
the index of the type used is first prepended, then the value is encoded.

\x01 \x00\x02
 (1)    (2)

(1): The index of the type in the different type arguments
(2): The actual encoded data
"""
import typing
import typing_extensions

import cain.types
import cain.types.numbers as numbers
from cain import errors
from cain.model import Datatype

T = typing_extensions.TypeVarTuple("T")


class Union(Datatype, typing.Generic[typing_extensions.Unpack[T]]):
    """
    Handles the encoding and decoding of union elements (elements which can be of different types)

    Example
    -------
    >>> Union.encode("Hello world", str)
    b'Hello world\x00'
    >>> Union.encode("Hello world", str, int)
    b'\x00Hello world\x00'
    >>> Union[str, int].encode(2)
    b'\x01\x00\x02'
    >>> from cain.types.numbers import Int, short
    >>> Union.encode(2, str, Int[short])
    b'\x01\x02'
    """

    @classmethod
    def _encode(cls, value: typing.Union[typing_extensions.Unpack[T]], *args):
        types_length = len(args)
        if types_length == 1:
            arg_type, type_args = cain.types.retrieve_type(args[0])
            return arg_type._encode(value, *type_args)

        int_encoder = numbers.recommended_size(types_length)

        current_type, _ = cain.types.retrieve_type(value.__class__)

        processed_types = []
        for index, arg in enumerate(args):
            arg_type, type_args = cain.types.retrieve_type(arg)
            if arg_type == current_type:
                return int_encoder._encode(index, *args) + arg_type._encode(value, *type_args)

            processed_types.append((arg_type, type_args))

        # Might be a subclass then
        types_names = []
        # print(processed_types)
        for index, (arg_type, type_args) in enumerate(processed_types):
            if issubclass(arg_type, current_type):
                return int_encoder._encode(index, *args) + arg_type._encode(value, *type_args)
            types_names.append(arg_type.__name__)

        raise errors.EncodingError(cls,
                                   "The given element does not seem to be of any "
                                   f"type mentionned in the Union (`{current_type.__name__}` is not in [{', '.join(types_names)}])")

    @classmethod
    def _decode(cls, value: bytes, *args):
        types_length = len(args)
        if types_length == 1:
            arg_type, type_args = cain.types.retrieve_type(args[0])
            return arg_type._decode(value, *type_args)

        int_encoder = numbers.recommended_size(types_length)
        type_index, value = int_encoder._decode(value, *args)
        current_type, type_args = cain.types.retrieve_type(args[type_index])
        return current_type._decode(value, *type_args)
