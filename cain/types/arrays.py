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
                current_type, current_type_args = cain.types.retrieve_type(arg)
                results.append((current_type, current_type_args))
            except (errors.UnknownTypeError, TypeError):
                continue
        return results

    @classmethod
    def _encode(cls, value: typing.Iterable[typing.Any], *args):
        value = list(value)  # normalize the available methods and fix its indices since the whole operation will eventually be O(n)

        types = cls.process_types_args(args)
        types_length = len(types)
        length = len(value)

        if types_length == 1:
            # list[int] with [1, 2, 3]
            result = cain.types.Int._encode(length, *args)
            types = [types[0]] * length

            integer_encoder = cain.types.Int
        else:
            if types_length != length:
                raise errors.EncodingError(cls,
                                           f"The given number of elements ({length})\
                                            is not matching the number of types provided in the model ({types_length})")
            # list[int, int, int] with [1, 2, 3]
            result = b""

            integer_encoder = cain.types.numbers.recommended_size(length)

        # pylint: disable=pointless-string-statement
        """
        \x01\x02\x03\x04  \x01\x02\x03\x04\x05 \x01\x02\x03\x03     \x01\x02\x03\x03          \x00\x00\x00\x00 \x00\x01\x02\x03\x04 ...
        ~~~~~~~~~~~~~~~~ [~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~ ... ~~~~~~~~~~~~~~~~ ...] ... ~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~ ...
        <  arr length  >  <   # of indices   > < red. ind. #1 >     <   red. data  >          <   end flag   > < unprocessed data   ...
        """

        results_table: dict[bytes, list[int]] = {
            # data: int(#of_appearance)
        }

        results = []

        for index, (current_type, type_args) in enumerate(types):
            data = current_type._encode(value[index], *type_args)

            try:
                results_table[data].append(index)
            except KeyError:
                results_table[data] = [index]

            results.append(data)

        _, integer_length = integer_encoder.process_args(args)

        redundancies_count = 0
        redundancies_result = b""
        redundancies_indices = []
        for data, indices in results_table.items():
            if len(indices) <= 1 or len(data) <= integer_length:
                # if there is only one occurence or it's not worth it
                continue
            redundancies_count += 1

            # Adding the indices
            redundancies_result += integer_encoder._encode(len(indices), *args)
            redundancies_result += b"".join(integer_encoder._encode(index, *args) for index in indices)
            # Adding the data
            redundancies_result += data
            redundancies_indices.extend(indices)

        result += integer_encoder._encode(redundancies_count, *args)
        result += redundancies_result

        for index, data in enumerate(results):
            if index in redundancies_indices:
                continue
            result += data

        return result

    @classmethod
    def _decode(cls, value: bytes, *args):
        types = cls.process_types_args(args)
        types_length = len(types)

        results = []

        if types_length == 1:
            length, value = cain.types.Int._decode(value, *args)
            types = [types[0]] * length
            integer_encoder = cain.types.numbers.Int
        else:
            length = types_length
            integer_encoder = cain.types.numbers.recommended_size(length)

        results = [None] * length

        processed_indices = []

        redundancy_header_length, value = integer_encoder._decode(value, *args)

        for _ in range(redundancy_header_length):
            # getting the number of times it appears in the array
            redundancy_count, value = integer_encoder._decode(value, *args)

            current_indices = []
            for _ in range(redundancy_count):
                # for each time, get its index
                index, value = integer_encoder._decode(value, *args)
                current_indices.append(index)
                processed_indices.append(index)

            # get the actual data, which follows the indices list

            try:
                index = current_indices[0]
                current_type, type_args = types[index]
                data, after_decoding = current_type._decode(value, *type_args)
                results[index] = data

                for index in current_indices[1:]:
                    current_type, type_args = types[index]  # could produce the same bytes while being two different datatypes
                    data, _ = current_type._decode(value, *type_args)
                    results[index] = data

                value = after_decoding
            except IndexError:
                pass

            continue

        for index, (current_type, type_args) in enumerate(types):
            if index in processed_indices:
                continue
            # if not already processed, then decode the actual value and add it
            data, value = current_type._decode(value, *type_args)
            results[index] = data

        return results, value


List = Array
