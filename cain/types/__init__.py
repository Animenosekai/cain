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
from .objects import Object


def retrieve_type(datatype: typing.Union[typing.Type[model.Datatype], type]) -> typing.Type[model.Datatype]:
    """
    Returns the right datatype
    """

    if isinstance(datatype, model.Datatype):
        return datatype.__class__

    datatype = typing.get_origin(datatype) or datatype

    if issubclass(datatype, model.Datatype):
        return datatype

    if issubclass(datatype, (set)) or datatype is typing.Set:
        return Set

    if issubclass(datatype, (tuple)) or datatype is typing.Tuple:
        return Tuple

    if issubclass(datatype, (list)) or datatype is typing.List:
        return Array

    if issubclass(datatype, (bool)):
        return Boolean

    if issubclass(datatype, (int)):
        return Int

    if issubclass(datatype, (float)):
        return Float

    if issubclass(datatype, (str)):
        return String

    if issubclass(datatype, (bytes)):
        return Binary

    raise errors.UnknownTypeError(datatype, f"The given datatype {datatype.__name__} is not known")
