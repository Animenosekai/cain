"""
types

Exports all of the natively available datatypes
"""

import typing
import cain.model as model
import cain.errors as errors

from .numbers import Number, Int, Float, Double
from .booleans import Boolean
from .binary import Binary
from .characters import Character
from .strings import String
from .arrays import Array
from .sets import Set
from .tuples import Tuple
from .optional import Optional
from .union import Union
from .nonetype import NoneType
from .ranges import Range
from .objects import Object


def retrieve_type(datatype: typing.Union[typing.Type[model.Datatype], type, model.Datatype]) -> typing.Tuple[typing.Type[model.Datatype], typing.List[typing.Union[str, typing.Type]]]:
    """
    Returns the right datatype
    """

    type_args = [current_type_arg.__forward_arg__
                 if isinstance(current_type_arg, typing.ForwardRef) else current_type_arg
                 for current_type_arg in typing.get_args(datatype)]

    if isinstance(datatype, model.Datatype):
        return datatype.__class__, datatype.args + type_args

    if None in type_args or type(None) in type_args:
        return Optional, type_args

    datatype = typing.get_origin(datatype) or datatype

    if datatype == typing.Union:
        return Union, type_args

    if datatype is None:
        return NoneType, type_args

    if issubclass(datatype, (range)):
        return Range, type_args

    if issubclass(datatype, model.Datatype):
        return datatype, type_args

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

    raise errors.UnknownTypeError(datatype, f"The given datatype {datatype.__name__} is not known")
