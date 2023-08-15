"""
arrays.py

Defines the Array datatype, which is used to store list of values.

Example
-------
>>> from cain.types import Array
>>> Array[int]([1, 2, 3]).encoded
b'\x00\x03\x00\x00\x00\x01\x00\x02\x00\x03'
>>> Array[int].encode([1, 2, 3])
b'\x00\x03\x00\x00\x00\x01\x00\x02\x00\x03'
>>> Array.encode([1, 2, 3], int)
b'\x00\x03\x00\x00\x00\x01\x00\x02\x00\x03'
>>> Array.decode(b'\x00\x03\x00\x00\x00\x01\x00\x02\x00\x03', int)
[1, 2, 3]
>>> Array.encode(["Hello", "Hi", "Hello", "Hey"], str)
b'\x00\x04\x00\x01\x00\x02\x00\x00\x00\x02Hello\x00Hi\x00Hey\x00'
>>> Array.encode(["Hello", 1], str, int)
b'\x00Hello\x00\x00\x01'
>>> Array[str, int, str].encode(["Hello", 1, "Yay"])
b'\x00Hello\x00\x00\x01Yay\x00'
>>> Array[str, int].encode(["Hello", 1, "Yay"], str)
b'\x00Hello\x00\x00\x01Yay\x00'

Structure
---------
Case 1: Without repetition in the data
Example: [1, 2, 3]

\x00\x03  \x00\x00   \x00\x01 \x00\x02 \x00\x03
~~~~~~~~  ~~~~~~~~   ~~~~~~~~~~~~~~~~~~~~~~~~~~
Array     Number     Rest of data
Length    of repeats

Case 2: With repetition in the data
Example: ["Hello", "Hi", "Hello", "Hey"]

\x00\x04   \x00\x01    \x00\x02 \x00\x00 \x00\x02 Hello\x00        Hi\x00 Hey\x00
~~~~~~~~   ~~~~~~~~   [~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~] * n   ~~~~~~~~~~~~~~
Array      Number of   Number    Index1   Index2  Repeated         Rest of data
Length     repeats     of indices                 Data
             (n)
"""
import typing
import typing_extensions

import cain.types
from cain import errors
from cain.model import Datatype

T = typing_extensions.TypeVarTuple("T")


class Array(Datatype, typing.Generic[typing_extensions.Unpack[T]]):
    """
    Handles the encoding and decoding of arrays.

    Example
    -------
    >>> Array[int].encode([1, 2, 3])
    b'\x00\x03\x00\x00\x00\x01\x00\x02\x00\x03'
    >>> Array.decode(b'\x00\x03\x00\x00\x00\x01\x00\x02\x00\x03', int)
    [1, 2, 3]
    """

    @staticmethod
    def process_types_args(args) -> typing.List[typing.Tuple[Datatype, typing.List]]:
        """
        Returns the right types in the array
        """
        results = []
        for arg in args:
            try:
                results.append(cain.types.retrieve_type(arg))
            except (errors.UnknownTypeError, TypeError):
                continue
        return results

    @classmethod
    def _encode(cls, value: typing.Iterable[typing.Any], *args):
        # normalize the available methods and
        # fix its indices since the whole operation
        # will eventually be O(n)
        value = list(value)

        types = cls.process_types_args(args)  # get the different types given
        types_length = len(types)
        length = len(value)

        if types_length == 1:
            # Case 1: Only a single type is given.
            # All of the elements will be of the same type.
            # Example: list[int] with [1, 2, 3]
            result = cain.types.numbers.UnsignedInt._encode(length, *args)
            types = [types[0]] * length

            # We are working with length and indices, which can't be negative.
            integer_encoder = cain.types.numbers.UnsignedInt
        else:
            # Case 2: Multiple types are given.
            # The number of types should match the number of elements.
            # Each element will be of the corresponding type.
            # Example: list[int, int, int] with [1, 2, 3]
            if types_length != length:
                raise errors.EncodingError(cls,
                                           f"The given number of elements ({length}) "
                                           f"is not matching the number of types provided in the model ({types_length})")
            result = b""
            # All of the encoded integers will be less or equal than the length of the array
            # We can optimize the size of the encoded integers
            integer_encoder = cain.types.numbers.recommended_size(length)

        # This is a table containing the data and the indices where the data appears
        results_table: dict[bytes, list[int]] = {}
        results = []

        for index, (current_type, type_args) in enumerate(types):
            data = current_type._encode(value[index], *type_args)

            try:
                results_table[data].append(index)
            except KeyError:
                # the data is new
                results_table[data] = [index]

            results.append(data)

        # Checking the size of the newly encoded integers because
        # we don't need to mark as a repeated value if it does not help with the end size
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
            redundancies_result += integer_encoder._encode(len(indices), *args)  # adding the number of indices
            redundancies_result += b"".join(integer_encoder._encode(index, *args) for index in indices)  # adding the actual indices
            # Adding the data
            redundancies_result += data  # adding the repeated data
            redundancies_indices.extend(indices)

        result += integer_encoder._encode(redundancies_count, *args)  # adding the number of repeated data
        result += redundancies_result  # adding the repeated data

        for index, data in enumerate(results):
            if index in redundancies_indices:
                continue
            # adding the rest of the data (which is not repeated)
            result += data

        return result

    @classmethod
    def _decode(cls, value: bytes, *args):
        types = cls.process_types_args(args)
        types_length = len(types)

        results = []

        if types_length == 1:
            # Case 1
            # Refer to the explanation in `_encode`
            length, value = cain.types.numbers.UnsignedInt._decode(value, *args)
            types = [types[0]] * length
            integer_encoder = cain.types.numbers.UnsignedInt
        else:
            # Case 2
            # Refer to the explanation in `_encode`
            length = types_length
            integer_encoder = cain.types.numbers.recommended_size(length)

        # Preparing an array
        # This is used to add elements non successively
        # Example: We can add things at index 1 then add another at index 20
        results = [None] * length

        processed_indices = []

        # Getting the number of repeated items
        redundancy_header_length, value = integer_encoder._decode(value, *args)

        # For each repeated item
        for _ in range(redundancy_header_length):
            # Getting the number of times it appears in the array
            redundancy_count, value = integer_encoder._decode(value, *args)

            current_indices = []
            # Get every indices of the repeated item
            for _ in range(redundancy_count):
                index, value = integer_encoder._decode(value, *args)
                current_indices.append(index)
                processed_indices.append(index)

            # Get the actual data, which follows the indices list
            # An `IndexError` might happen if `redundancy_count` is 0.
            # Because `try...catch` blocks are expensive, we won't be checking this case.
            # Therefore, repeats present in 0 locations in the array are prohibited.
            index = current_indices[0]
            current_type, type_args = types[index]
            # Decoding the data for the first index
            data, after_decoding = current_type._decode(value, *type_args)
            results[index] = data

            # Decoding the data for the rest of the indices
            for index in current_indices[1:]:
                # We can't use the same datatype as two different datatypes
                # can produce the same encoded bytes.
                # Example: `Array`, `Tuple` and `Set`
                current_type, type_args = types[index]
                # We already removed the bytes corresponding to the data the first time,
                # so we don't need to remove it again.
                data, _ = current_type._decode(value, *type_args)
                results[index] = data

            value = after_decoding
            continue

        for index, (current_type, type_args) in enumerate(types):
            if index in processed_indices:
                continue
            # If not already processed, then decode the actual value and add it
            data, value = current_type._decode(value, *type_args)
            results[index] = data

        return results, value

List = Array
