"""
objects.py

Defines the objects datatype.
"""
import typing

import cain.types
from cain.model import Datatype


class Object(Datatype, dict):
    """
    A basic object to hold multiple values

    Example
    -------
    >>> from cain.types import Object
    >>> class TestObject(Object):
    ...     username: str
    ...     favorite_number: int

    >>> TestObject({"username": "test1", "favorite_number": 2})
    TestObject(...)
    >>> TestObject(username="test1", favorite_number=2)
    TestObject(...)
    """

    def __init__(self, *args, **kwargs) -> None:
        value = {}
        for element in args:
            value.update(element)
        value.update(kwargs)
        super().__init__(value)

    def __getattribute__(self, name: str) -> typing.Any:
        # TODO: Make this at the `Datatype` level ?
        # TODO: Datatype.__getattribute__ doesn't work
        try:
            return Datatype.__getattribute__(self, name)
        except AttributeError:
            try:
                return getattr(self.value, name)
            except AttributeError:
                return self.value[name]

    @staticmethod
    def process_type(type):
        """
        Processes the given type to return the proper datatype and type args
        """
        try:
            args = [arg.__forward_arg__ if isinstance(arg, typing.ForwardRef) else arg for arg in typing.get_args(type)]
        except Exception:
            args = ()
        return cain.types.retrieve_type(type), args

    @classmethod
    def encode(cls, value: dict, *args):
        result = b""

        types = sorted(cls.__annotations__.items(), key=lambda item: item[0])

        # pylint: disable=pointless-string-statement
        """
        \x00\x00\x00\x00 \x01\x02\x03\x04\x05 \x01\x02\x03\x03     \x01\x02\x03\x03          \x00\x01\x02\x03\x04 ...
        ~~~~~~~~~~~~~~~~ [~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~ ... ~~~~~~~~~~~~~~~~ ...] ... ~~~~~~~~~~~~~~~~~~~~ ...
        <   # of red.  >  <   # of indices   > < red. ind. #1 >     <   red. data  >          < unprocessed data   ...
        """

        results_table: dict[bytes, list[int]] = {
            # data: int(#of_appearance)
        }

        results = []

        for index, (key, current_type) in enumerate(types):
            current_type, type_args = cls.process_type(current_type)
            data = current_type.encode(value[key], *type_args)

            try:
                results_table[data].append(index)
            except KeyError:
                results_table[data] = [index]

            results.append(data)

        redundancies_indices = []

        integer_length = len(cain.types.Int.encode(0, *args))

        redundancies_count = 0

        redundancies_result = b""

        for data, indices in results_table.items():
            if len(indices) <= 1 or len(data) <= integer_length:
                # if there is only one occurence or it's not worth it
                continue
            redundancies_count += 1

            # Adding the indices
            redundancies_result += cain.types.Int.encode(len(indices), *args)
            redundancies_result += b"".join(cain.types.Int.encode(index, *args) for index in indices)
            # Adding the data
            redundancies_result += data
            redundancies_indices.extend(indices)

        result += cain.types.Int.encode(redundancies_count, *args)
        result += redundancies_result

        for index, data in enumerate(results):
            if index in redundancies_indices:
                continue

            result += data

        return result

    @classmethod
    def decode(cls, value: bytes, *args):
        results = {}
        types = sorted(cls.__annotations__.items(), key=lambda item: item[0])

        processed_indices = []

        redundancy_header_length, value = cain.types.Int.decode(value, *args)

        for _ in range(redundancy_header_length):
            # getting the number of times it appears in the array
            redundancy_count, value = cain.types.Int.decode(value, *args)

            current_indices = []
            for _ in range(redundancy_count):
                # for each time, get its index
                index, value = cain.types.Int.decode(value, *args)
                current_indices.append(index)
                processed_indices.append(index)

            # get the actual data, which follows the indices list

            try:
                index = current_indices[0]
                key, current_type = types[index]
                current_type, type_args = cls.process_type(current_type)
                data, after_decoding = current_type.decode(value, *type_args)
                results[key] = data
            except IndexError:
                after_decoding = value

            for index in current_indices[1:]:
                key, current_type = types[index]  # could produce the same bytes while being two different datatypes
                current_type, type_args = cls.process_type(current_type)
                data, _ = current_type.decode(value, *type_args)
                results[key] = data

            value = after_decoding

            continue

        for index, (key, current_type) in enumerate(types):
            if index in processed_indices:
                continue
            # if not already processed, then decode the actual value and add it
            current_type, type_args = cls.process_type(current_type)
            data, value = current_type.decode(value, *type_args)
            results[key] = data

        return results, value
