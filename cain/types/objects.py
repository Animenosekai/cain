"""
objects.py

Defines the Object datatype, which is used to store dictionaries.

Example
-------
>>> from cain.types import Object
>>> class TestObject(Object):
...     username: str
...     favorite_number: int
>>> TestObject(username="Anise", favorite_number=2)
TestObject({'username': 'Anise', 'favorite_number': 2})
>>> TestObject({"username": "Anise", "favorite_number": 2})
TestObject({'username': 'Anise', 'favorite_number': 2})
>>> TestObject({"username": "Anise"}, favorite_number=2)
TestObject({'username': 'Anise', 'favorite_number': 2})
>>> TestObject.encode({"username": "Anise", "favorite_number": 2})
b'\x00\x00\x00\x02Anise\x00'
>>> TestObject.decode(b'\x00\x00\x00\x02Anise\x00')
{'favorite_number': 2, 'username': 'Anise'}
>>> class TestObject2(Object):
...     name: str
...     username: str
...     favorite_number: int
>>> TestObject2.encode({"name": "Anise", "username": "Anise", "favorite_number": 2})
b'\x00\x01\x00\x02\x00\x01\x00\x02Anise\x00\x00\x02'

Structure
---------
Note: Any index in the encoded data is the index of a key in the sorted list of keys.

Case 1: No repetition in the data
Example: {"username": "Anise", "favorite_number": 2}

\x00\x00   \x00\x02 Anise\x00
~~~~~~~~   ~~~~~~~~~~~~~~~~~·
Number     Rest of data
of repeats

Case 2: With a repetition in the data
Example: {"name": "Anise", "username": "Anise", "favorite_number": 2}

\x00\x01    \x00\x02 \x00\x01 \x00\x02 Anise\x00        \x00\x02
~~~~~~~~   [~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~] * n   ~~~~~~~~~~~~~~
Number of   Number    Index1   Index2  Repeated         Rest of data
repeats     of indices                 Data
(n)

Note: Unlike Arrays we don't need to encode the length because it is fixed.
"""
import typing

import cain.types
from cain.model import Datatype


class Object(Datatype):
    """
    An object which handles the encoding and use of dictionaries.

    Example
    -------
    >>> class TestObject(Object):
    ...     username: str
    ...     favorite_number: int
    >>> TestObject(username="Anise", favorite_number=2)
    TestObject({'username': 'Anise', 'favorite_number': 2})
    >>> TestObject({"username": "Anise", "favorite_number": 2})
    TestObject({'username': 'Anise', 'favorite_number': 2})
    >>> TestObject({"username": "Anise"}, favorite_number=2)
    TestObject({'username': 'Anise', 'favorite_number': 2})
    >>> TestObject.encode({"username": "Anise", "favorite_number": 2})
    b'\x00\x00\x00\x02Anise\x00'
    >>> TestObject.decode(b'\x00\x00\x00\x02Anise\x00')
    {'favorite_number': 2, 'username': 'Anise'}
    >>> class TestObject2(Object):
    ...     name: str
    ...     username: str
    ...     favorite_number: int
    >>> TestObject2.encode({"name": "Anise", "username": "Anise", "favorite_number": 2})
    b'\x00\x01\x00\x02\x00\x01\x00\x02Anise\x00\x00\x02'
    """

    def __init__(self, value: typing.Optional[dict] = None, *args, **kwargs) -> None:
        value = value or {}
        value.update(kwargs)
        super().__init__(value, *args)

    def __getattr__(self, key: str):
        if key == "_cain_value":
            return super().__getattribute__("_cain_value")

        try:
            return super().__getattr__(key)
        except AttributeError as err:
            try:
                return self[key]
            except KeyError as exc:
                raise err from exc

    @classmethod
    def _encode(cls, value: dict, *args):
        result = b""
        types = sorted(cls.__type_hints__.items(), key=lambda item: item[0])
        # Because we are working with integers less or equal than a fixed length,
        # we can optimize the size of the encoded integers.
        integer_encoder = cain.types.numbers.recommended_size(len(types))

        # This is a table containing the data and the indices where the data appears
        results_table: dict[bytes, list[int]] = {}
        results = []

        for index, (key, current_type) in enumerate(types):
            current_type, type_args = cain.types.retrieve_type(current_type)
            data = current_type._encode(value[key], *type_args)

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
        results = {}
        types = sorted(cls.__type_hints__.items(), key=lambda item: item[0])
        # Getting the right integer decoder
        integer_encoder = cain.types.numbers.recommended_size(len(types))

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
            key, current_type = types[index]
            current_type, type_args = cain.types.retrieve_type(current_type)
            # Decoding the data for the first index
            data, after_decoding = current_type._decode(value, *type_args)
            results[key] = data

            # Decoding the data for the rest of the indices
            for index in current_indices[1:]:
                # We can't use the same datatype as two different datatypes
                # can produce the same encoded bytes.
                # Example: `Array`, `Tuple` and `Set`
                key, current_type = types[index]
                current_type, type_args = cain.types.retrieve_type(current_type)
                # We already removed the bytes corresponding to the data the first time,
                # so we don't need to remove it again.
                data, _ = current_type._decode(value, *type_args)
                results[key] = data

            value = after_decoding
            continue

        for index, (key, current_type) in enumerate(types):
            if index in processed_indices:
                continue
            # If not already processed, then decode the actual value and add it
            current_type, type_args = cain.types.retrieve_type(current_type)
            data, value = current_type._decode(value, *type_args)
            results[key] = data

        return cls(results), value


Dict = Object
