"""
arrays.py

Defines the Array datatype
"""
import typing

from cain import errors
from cain.model import Datatype
import cain.types

T = typing.TypeVarTuple("T")


class Array(Datatype, typing.Generic[*T]):
    """
    Handles the encoding and decoding of arrays.
    """

    @staticmethod
    def process_types_args(args) -> typing.List[typing.Tuple[Datatype, typing.List]]:
        """
        Returns the right types in the array
        """
        results = []
        for arg in args:
            try:
                current_type = cain.types.retrieve_type(arg)
                try:
                    current_type_args = [current_type_arg.__forward_arg__
                                         if isinstance(current_type_arg, typing.ForwardRef) else current_type_arg
                                         for current_type_arg in typing.get_args(arg)]
                except Exception:
                    current_type_args = []
                results.append((current_type, current_type_args))
            except (errors.UnknownTypeError, TypeError):
                continue
        return results

    @classmethod
    def encode(cls, value: typing.Iterable[typing.Any], *args):
        value = list(value)  # normalize the available methods and fix its indices since the whole operation will eventually be O(n)

        types = cls.process_types_args(args)
        types_length = len(types)
        length = len(value)

        if types_length != length:
            if types_length != 1:  # everything is of type `types[0]`
                raise errors.EncodingError(
                    cls, f"The given number of elements ({length}) is not matching the number of types provided in the model ({types_length})")

            # list[int] with [1, 2, 3]
            result = cain.types.Int.encode(length, *args)
            current_type, type_args = types[0]

            for element in value:
                result += current_type.encode(element, *type_args)

            return result

        # list[int, int, int] with [1, 2, 3]
        result = b""
        for index, (current_type, type_args) in enumerate(types):
            result += current_type.encode(value[index], *type_args)
        return result

    @classmethod
    def decode(cls, value: bytes, *args):
        types = cls.process_types_args(args)
        types_length = len(types)

        results = []

        if types_length == 1:
            length, value = cain.types.Int.decode(value, *args)
            current_type, type_args = types[0]

            for _ in range(length):
                result, value = current_type.decode(value, *type_args)
                results.append(result)
            return results, value

        results = []
        for (current_type, type_args) in types:
            result, value = current_type.decode(value, *type_args)
            results.append(result)
        return results, value


List = Array
