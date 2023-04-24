"""
objects.py

Defines the objects datatype.
"""
import typing

import cain.types
from cain.model import Datatype


class Object(Datatype):
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

    @classmethod
    def encode(cls, value: dict, *args):
        data = b""
        for key in sorted(cls.__annotations__.keys()):
            current_type = cls.__annotations__[key]
            try:
                args = [arg.__forward_arg__ if isinstance(arg, typing.ForwardRef) else arg for arg in typing.get_args(current_type)]
            except Exception:
                args = ()
            data += cain.types.retrieve_type(current_type).encode(value[key], *args)
            # KeyError if forgetting a value
        return data

    @classmethod
    def decode(cls, value: bytes, *args):
        data = {}
        for key in sorted(cls.__annotations__.keys()):
            current_type = cls.__annotations__[key]
            try:
                args = typing.get_args(current_type)
            except Exception:
                args = ()
            current_val, value = cain.types.retrieve_type(current_type).decode(value, *args)
            data[key] = current_val
        return data, value
