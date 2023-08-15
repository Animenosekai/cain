"""
types.py

Defines the Type datatype, which is used to encode datatypes

Example
-------
>>> from cain.types.types import Type
>>> Type.encode(str)
b'\x01\x03\x00\x01\x02\x00\x00\x00\x00\x1a'
>>> Type.decode(b'\x01\x03\x00\x01\x02\x00\x00\x00\x00\x1a')
String

Structure
---------
"""
from __future__ import annotations

import typing
import cain.types
import cain.model

Schema = typing.Union[typing.Type[cain.model.Datatype], cain.model.Datatype, typing.Type]


class Type(cain.types.Object):
    """
    Handles the encoding and decoding of types elements.

    Example
    -------
    >>> from cain.types.types import Type
    >>> Type.encode(str)
    b'\x01\x03\x00\x01\x02\x00\x00\x00\x00\x1a'
    >>> Type.decode(b'\x01\x03\x00\x01\x02\x00\x00\x00\x00\x1a')
    String
    """

    index: cain.types.UInt8
    """The index of the Datatype in `TYPES_REGISTRY`"""
    name: typing.Optional[str] = None
    """If changed, the name of the Datatype"""
    annotations_keys: list[str]
    """The keys for the annotations, in the order they appear in `annotations_values`"""
    annotations_values: list[Type]
    """The values for the annotations, in the order they appear in `annotations_values`"""
    arguments: list[typing.Union[str, Type]]
    """The different type arguments"""

    @classmethod
    def pack(cls, value: Schema, json: bool = False):
        """Packs the given type in a dictionary"""
        datatype, type_args = cain.types.retrieve_type(value)
        datatype_annotations = datatype.__type_hints__
        type_name = datatype.__name__
        if issubclass(datatype, cain.types.Object):
            datatype = cain.types.Object
        result = {
            "index": TYPES_REGISTRY.index(repr(datatype)),
            "name": type_name if type_name != datatype.__name__ else None,
            "annotations_keys": list(datatype_annotations.keys()),
            "annotations_values": list(datatype_annotations.values()),
            "arguments": list(type_args)
        }
        if json:
            result["annotations_values"] = [Type.pack(val, json=True) for val in result["annotations_values"]]
            result["arguments"] = [Type.pack(val, json=True) if not isinstance(val, str) else val
                                   for val in result["arguments"]]
            # JSON exclusive
            result["datatype"] = repr(datatype)
        return result

    @classmethod
    def _encode(cls, value: Schema, *args):
        return super()._encode(cls.pack(value), *args)

    @classmethod
    def unpack(cls, data: dict) -> typing.Type[cain.model.Datatype]:
        """Creates a Datatype from the given value"""
        type_name = TYPES_REGISTRY[data["index"]]
        if type_name == "Type":
            new_type = Type
        else:
            new_type: typing.Type = getattr(cain.types, type_name)

        class NewType(new_type):
            """A subclass containing the type arguments"""
            __annotations__ = {key: data["annotations_values"][index]
                               for index, key in enumerate(data["annotations_keys"])}
            __args__ = data["arguments"]

        NewType.__name__ = data["name"] if data["name"] else new_type.__name__
        return NewType

    @classmethod
    def _decode(cls, value: bytes, *args):
        data, value = super()._decode(value, *args)
        return cls.unpack(data), value

    @classmethod
    def lookup(cls, value: bytes, *args) -> typing.Dict[str, typing.Any]:
        """Looks up inside the encoded type"""
        data, value = super()._decode(value, *args)
        return data


# Note: New types should be added at the end of the
# registry for backward compatibility

TYPES_REGISTRY = [
    "Array",
    "Binary",
    "Boolean",
    "Character",
    "NoneType",
    "Number",
    "Int",
    "Float",
    "Double",
    "Decimal",
    "Complex",
    "DoubleComplex",
    "SignedInt",
    "UnsignedInt",
    "Int8",
    "UInt8",
    "Int16",
    "UInt16",
    "Int32",
    "UInt32",
    "Int64",
    "UInt64",
    "Object",
    "Optional",
    "Range",
    "Set",
    "String",
    "Tuple",
    "Type",
    "Union",
    "Enum"
]
