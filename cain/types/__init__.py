"""
types

Exports all of the natively available datatypes
"""

import typing
import cain.model as model
import cain.errors as errors

from .characters import Character
from .strings import String
from .numbers import Number, Int, Float, Double, Decimal
from .numbers import Complex, DoubleComplex
from .numbers import SignedInt, UnsignedInt, Int8, UInt8, Int16, UInt16, Int32, UInt32, Int64, UInt64
from .nonetype import NoneType
from .optionals import Optional
from .unions import Union
from .booleans import Boolean, Bool
from .binary import Binary
from .arrays import Array, List
from .sets import Set
from .tuples import Tuple
from .ranges import Range
from .objects import Object, Dict
from .enums import Enum


# from .types import Type, TYPES_REGISTRY

NONE_TYPE = type(None)


def retrieve_type(datatype: typing.Union[typing.Type[model.Datatype],
                                         type,
                                         model.Datatype]) -> typing.Tuple[typing.Type[model.Datatype],
                                                                          typing.List[typing.Union[str, typing.Type]]]:
    """
    Returns the right datatype
    """

    if hasattr(datatype, "__args__"):
        type_args = datatype.__args__
    else:
        type_args = [current_type_arg.__forward_arg__
                     if isinstance(current_type_arg, typing.ForwardRef) else current_type_arg
                     for current_type_arg in typing.get_args(datatype)]

    if isinstance(datatype, model.Datatype):
        return datatype.__class__, datatype.args + type_args

    if None in type_args or type(None) in type_args:
        return Optional, type_args

    datatype = typing.get_origin(datatype) or datatype

    if datatype is typing.Union:
        return Union, type_args

    if datatype is None or datatype is NONE_TYPE:
        return NoneType, type_args

    if issubclass(datatype, (range)):
        return Range, type_args

    if issubclass(datatype, model.Datatype):
        return datatype.__root__, type_args

    if issubclass(datatype, (set)) or datatype is typing.Set:
        return Set, type_args

    if issubclass(datatype, (tuple)) or datatype is typing.Tuple:
        return Tuple, type_args

    if issubclass(datatype, (list)) or datatype is typing.List:
        return Array, type_args

    if issubclass(datatype, (dict)) or datatype is typing.Dict:
        return Object, type_args

    if issubclass(datatype, (bool)):
        return Boolean, type_args

    if issubclass(datatype, (int)):
        return Int, type_args

    if issubclass(datatype, (float)):
        return Float, type_args

    if issubclass(datatype, (str)):
        return String, type_args

    if issubclass(datatype, (bytes)):
        return Binary, type_args

    if issubclass(datatype, type) or datatype is typing.Type:
        from .types import Type
        return Type, type_args

    raise errors.UnknownTypeError(datatype, f"The given datatype `{datatype.__name__}` is not known")
