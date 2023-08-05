"""
Pydantic-compatible field types for [Pandas](https://pypi.org/project/pandas/) series and dataframe objects.

This module contains classes that provide Pydantic-compatible field types specifically tailored for Pandas series
and dataframe objects.
These custom fields allow developers to enforce specific data types including their physical dimensionality and the
index type.
"""

from __future__ import annotations

import inspect
from numbers import Number
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Generic, Iterable, Optional, Sequence, Type, TypeVar, Union, cast

import numpy as np
import pandas as pd
import pydantic
from pandas import Index
from pint_pandas import PintArray
from pydantic import ValidationError
from pydantic.fields import ModelField

from optool.fields.util import (WrongTypeError, check_sub_fields_level, get_subfield_schema, get_type_validator,
                                update_object_schema)
from optool.uom import PhysicalDimension, Quantity

T = TypeVar("T")
"""Type variable without an upper bound, specifying the type of the data of {py:class}`pandas.Series`."""

_PANDAS_INDEX_TYPES: Dict[str, Type[pd.Index]] = dict(
    inspect.getmembers(pd, lambda member: inspect.isclass(member) and issubclass(member, pd.Index)))

_R = TypeVar("_R", pd.Series, pd.DataFrame)


def _validate_index_type(val: _R, expected_index_type_name: Optional[str]) -> _R:
    if expected_index_type_name is None:
        return val

    if (expected_index_type := _PANDAS_INDEX_TYPES.get(expected_index_type_name, None)) is None:
        raise ValueError(f"The index type specified ({expected_index_type_name}) is not a valid pandas index. "
                         f"Valid index types are {list(_PANDAS_INDEX_TYPES.keys())}.")

    if isinstance(val.index, expected_index_type):
        return val
    raise IndexTypeError(expected=expected_index_type, value=val)


class ConstrainedSeries(pydantic.BaseModel, Generic[T]):
    """
    Pydantic-compatible field type for {py:class}`pandas.Series` objects, which allows to specify the data-type.

    :::{seealso}
    [Pydantic documentation: Custom Data Types](https://docs.pydantic.dev/usage/types/#custom-data-types) and
    {py:class}`pydantic.types.ConstrainedInt` or similar of {py:mod}`pydantic`
    :::
    """

    strict: ClassVar[bool] = True
    index_type: ClassVar[Optional[str]] = 'RangeIndex'

    @classmethod
    def __get_validators__(cls):
        yield get_type_validator(pd.Series) if cls.strict else cls.validate_series
        yield cls.validate_index_type
        yield cls.validate_dimensionality
        yield cls.validate_data_type

    @classmethod
    def __modify_schema__(cls, field_schema, field: Optional[ModelField]):
        update_object_schema(field_schema, index_type=cls.index_type, datatype=get_subfield_schema(field, 0))

    @classmethod
    def validate_series(cls, val: Any, field: ModelField) -> pd.Series:
        if isinstance(val, pd.Series):
            return val
        if not field.sub_fields:
            return pd.Series(val)

        if isinstance(val, Sequence) and len(val) == 2 and isinstance(val[1], Index):
            index = val[1]
            val = val[0]
        else:
            index = None

        check_sub_fields_level(field)
        data_type = field.sub_fields[0].type_

        if cls._is_physical_dimension(field.sub_fields[0]):
            # Now, we assume the output should have units
            pre_parsed_scalar_types = (str, Number, np.ndarray, Iterable)
            if isinstance(val, pre_parsed_scalar_types):
                try:
                    val = Quantity(val)
                except Exception as e:
                    raise WrongTypeError(expected=pre_parsed_scalar_types, value=val) from e

            val = cls._make_iterable_quantity(val)
            try:
                pint_array = PintArray(val)
            except Exception as e:
                raise ValueError(f"Cannot create a {PintArray.__name__} from {val}.") from e
            try:
                return pd.Series(pint_array, index=index)
            except Exception as e:
                raise ValueError(f"Cannot create a {pd.Series.__name__} from {PintArray.__name__} due to {e!r}.") from e

        # Validate each element separately
        valid_value = []
        iterable = cls._make_iterable_quantity(val) if isinstance(val, Iterable) else [val]
        for (i, el) in enumerate(iterable):
            valid_element, error = field.sub_fields[0].validate(el, {}, loc=f'element_{i}')
            if error:
                raise ValidationError([error], cls)
            valid_value.append(valid_element)

        return pd.Series(valid_value, index=index, dtype=data_type)

    @classmethod
    def validate_index_type(cls, val: pd.Series, field: ModelField) -> pd.Series:
        return _validate_index_type(val, cls.index_type)

    @classmethod
    def validate_dimensionality(cls, val: pd.Series, field: ModelField) -> pd.Series:
        if not field.sub_fields or not cls._is_physical_dimension(field.sub_fields[0]):
            return val

        if not isinstance(val.array, PintArray):
            raise WrongTypeError(expected=PintArray, value=val.array)

        dimension = field.sub_fields[0].type_
        if dimension == Any or cast(PintArray, val.array).quantity.check(dimension.dimensionality):
            return val

        raise DimensionalityError(expected=dimension.dimensionality, value=val)

    @classmethod
    def validate_data_type(cls, val: pd.Series, field: ModelField) -> pd.Series:
        if not field.sub_fields or cls._is_physical_dimension(field.sub_fields[0]):
            return val

        data_type = field.sub_fields[0].type_
        if val.dtype == data_type:
            return val

        raise WrongTypeError(expected=data_type, value=val.dtype)

    @classmethod
    def _make_iterable_quantity(cls, val: Any):
        if isinstance(val, Quantity) and not isinstance(val.magnitude, Iterable):
            val = Quantity([val.m], val.u)
        return val

    @classmethod
    def _is_physical_dimension(cls, field: ModelField) -> bool:
        return field.type_ == Any or issubclass(field.type_, PhysicalDimension)


class ConstrainedDataFrame:
    """
    Pydantic-compatible field type for {py:class}`pandas.DataFrame` objects, which allows to specify the index type.

    :::{seealso}
    [Pydantic documentation: Custom Data Types](https://docs.pydantic.dev/usage/types/#custom-data-types) and
    {py:class}`pydantic.types.ConstrainedInt` or similar of {py:mod}`pydantic`
    :::
    """

    strict: bool = True
    index_type: ClassVar[Optional[str]] = 'RangeIndex'

    @classmethod
    def __get_validators__(cls):
        yield get_type_validator(pd.DataFrame) if cls.strict else cls.validate_dataframe
        yield cls.validate_index_type

    @classmethod
    def __modify_schema__(cls, field_schema, field: Optional[ModelField]):
        update_object_schema(field_schema, index_type=cls.index_type)

    @classmethod
    def validate_dataframe(cls, val: Any, field: ModelField) -> pd.DataFrame:
        if isinstance(val, pd.DataFrame):
            return val
        if field.sub_fields:
            raise TypeError(f"A constrained DataFrame cannot by typed, but have sub-fields {field.sub_fields}")

        return pd.DataFrame(val)

    @classmethod
    def validate_index_type(cls, val: pd.DataFrame, field: ModelField) -> pd.DataFrame:
        return _validate_index_type(val, cls.index_type)


class IndexTypeError(ValueError):
    """
    Raised when the type of index of a {py:class}`pandas.Series` or {py:class}`pandas.DataFrame` object does not meet
    the expectations.

    :param expected: The expected type of the index.
    :param value: The series or dataframe that causes the error due to its index type.
    """

    def __init__(self, *, expected: Type[Index], value: Union[pd.Series, pd.DataFrame]) -> None:
        type_name = value.__class__.__name__
        super().__init__(f"expected index type {expected}, but got a {type_name} with index type {type(value.index)}")


class DimensionalityError(ValueError):
    """
    Raised when the dimensionality of a {py:class}`pandas.Series` does not meet the expectations.

    :param expected: The expected dimensionality.
    :param value: The series that causes the error due to its dimensionality.
    """

    def __init__(self, *, expected: str, value: pd.Series) -> None:
        super().__init__(f"expected the dimensionality {expected}, but got a series with data-type {value.dtype}")


if TYPE_CHECKING:
    SeriesLike = pd.Series
    DatetimeSeries = pd.Series
    TimedeltaSeries = pd.Series

    DataFrameLike = pd.DataFrame
    DatetimeDataFrame = pd.DataFrame
    TimedeltaDataFrame = pd.DataFrame
else:

    class SeriesLike(ConstrainedSeries[T]):
        """
        Pydantic-compatible field type for {py:class}`pandas.Series` objects.

        Assigned values not already of type {py:class}`~pandas.Series` are parsed using
        {py:class}`Series(val) <pandas.Series>`. If a {py:class}`~optool.uom.PhysicalDimension` is specified as generic
        type annotation, a {py:class}`pint_pandas.PintArray` is created and the corresponding dimensionality is
        verified. If the generic type annotation is different, the validation and parsing of each data element is
        forwarded to the specific type specified, e.g., in the example above, the value is validated using the
        implementation provided by {py:class}`pydantic.PositiveInt`.
        """
        strict = False

    class DatetimeSeries(ConstrainedSeries[T]):
        """
        Pydantic-compatible field type for {py:class}`pandas.Series` objects, the index of which must be of type
        {py:class}`~pandas.DatetimeIndex`.

        Assigned values not already of type {py:class}`~pandas.Series` are parsed using
        {py:class}`Series(val) <pandas.Series>`. If a {py:class}`~optool.uom.PhysicalDimension` is specified as generic
        type annotation, a {py:class}`pint_pandas.PintArray` is created and the corresponding dimensionality is
        verified. If the generic type annotation is different, the validation and parsing of each data element is
        forwarded to the specific type specified, e.g., in the example above, the value is validated using the
        implementation provided by {py:class}`pydantic.PositiveInt`.
        """
        strict = False
        index_type = 'DatetimeIndex'

    class TimedeltaSeries(ConstrainedSeries[T]):
        """
        Pydantic-compatible field type for {py:class}`pandas.Series` objects, the index of which must be of type
        {py:class}`~pandas.TimedeltaIndex`.

        Assigned values not already of type {py:class}`~pandas.Series` are parsed using
        {py:class}`Series(val) <pandas.Series>`. If a {py:class}`~optool.uom.PhysicalDimension` is specified as generic
        type annotation, a {py:class}`pint_pandas.PintArray` is created and the corresponding dimensionality is
        verified. If the generic type annotation is different, the validation and parsing of each data element is
        forwarded to the specific type specified, e.g., in the example above, the value is validated using the
        implementation provided by {py:class}`pydantic.PositiveInt`.
        """
        strict = False
        index_type = 'TimedeltaIndex'

    class DataFrameLike(ConstrainedDataFrame):
        """
        Pydantic-compatible field type for {py:class}`~pandas.DataFrame` objects.

        Assigned values not already of type {py:class}`~pandas.DataFrame` are parsed using the regular constructor
        {py:class}`DataFrame(val) <pandas.DataFrame>`.
        """
        strict = False

    class DatetimeDataFrame(ConstrainedDataFrame):
        """
        Pydantic-compatible field type for {py:class}`~pandas.DataFrame` objects, the index of which must be of type
        {py:class}`~pandas.DatetimeIndex`.

        Assigned values not already of type {py:class}`~pandas.DataFrame` are parsed using the regular constructor
        {py:class}`DataFrame(val) <pandas.DataFrame>`.
        """
        strict = False
        index_type = 'DatetimeIndex'

    class TimedeltaDataFrame(ConstrainedDataFrame):
        """
        Pydantic-compatible field type for {py:class}`~pandas.DataFrame` objects, the index of which must be of type
        {py:class}`~pandas.TimedeltaIndex`.

        Assigned values not already of type {py:class}`~pandas.DataFrame` are parsed using the regular constructor
        {py:class}`DataFrame(val) <pandas.DataFrame>`.
        """
        strict = False
        index_type = 'TimedeltaIndex'
