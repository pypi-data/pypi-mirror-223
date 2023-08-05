"""
Pydantic-compatible field types for data containers such as lists.

This module offers functionalities to create and manage typed and constrained containers that allow type checking and
validation. This ensures that data integrity is maintained as elements are added or manipulated within the container.
"""

import types
import typing
from typing import TYPE_CHECKING, Callable, Iterable, List, Optional, Type, TypeVar, Union, get_args

import pydantic
from pydantic import ValidationError, validate_model
from pydantic.error_wrappers import ErrorWrapper

from optool.core import BaseModel
from optool.fields.util import ValidationFunc

T = TypeVar("T")
"""Type variable without an upper bound, specifying the type of the elements of a constrained list."""

# Define _CustomList as a workaround for: https://github.com/python/mypy/issues/11427
#
# According to this issue, the typeshed contains a "white lie" (it adds MutableSequence to the ancestry of list), which
# completely messes with the type inference.

if TYPE_CHECKING:
    # Importing from builtins is preferred over simple assignment, see issues:
    # https://github.com/python/mypy/issues/8715
    # https://github.com/python/mypy/issues/10068
    # noinspection PyPep8Naming
    from builtins import list as _CustomList
else:
    from collections.abc import MutableSequence

    class _CustomList(MutableSequence, list):
        """Adds MutableSequence mixin while pretending to be a builtin list."""
        pass


def _create_list_model(**kwargs) -> Type[BaseModel]:

    class _ListModel(BaseModel):
        constrained_list: pydantic.types.conlist(**kwargs)  # type: ignore[valid-type]

    return _ListModel


class ConstrainedMutatingList(_CustomList[T]):
    """
    Typed container that runs validation when an element is added to the list.

    This ability provides runtime assurance that all elements adhere to specified conditions, which may include checks
    such as type compliance, value range, or any custom-defined criteria.

    :::{seealso}
    https://github.com/pydantic/pydantic/issues/496#issuecomment-904308727
    :::
    """
    min_items: Optional[int] = None
    max_items: Optional[int] = None
    custom_validators: Union[ValidationFunc, Iterable[ValidationFunc], None] = None

    _ListModel = None

    def __init_subclass__(cls) -> None:
        # Get the generic type. Approach taken from https://stackoverflow.com/a/71720366
        # noinspection PyUnresolvedReferences
        cls_item_type = get_args(cls.__orig_bases__[0])[0]  # type: ignore[attr-defined]
        cls._ListModel = _create_list_model(item_type=cls_item_type, min_items=cls.min_items, max_items=cls.max_items)

    def __init__(self, lst):
        (values, fields_set, error) = validate_model(self._ListModel, dict(constrained_list=lst))
        if error:
            raise error
        super().__init__(lst)

    def __len__(self):
        return list.__len__(self)

    def __getitem__(self, i):
        return list.__getitem__(self, i)

    def __delitem__(self, i):
        self._validate_and_apply(lambda x: x.__delitem__(i))

    def __setitem__(self, i, v):
        self._validate_and_apply(lambda x: x.__setitem__(i, v))

    def insert(self, i, v):
        self._validate_and_apply(lambda x: x.insert(i, v))

    def _validate_and_apply(self, operation: Callable[[list], None]):
        copy = self.copy()
        operation(copy)
        if self._ListModel is None:
            raise ValueError(f"The class of this model ({self.__class__}) has not internal list model.")
        values, fields_set, error = validate_model(self._ListModel, dict(constrained_list=copy))
        if error:
            raise error

        validated_values = values['constrained_list']
        if self.custom_validators:
            try:
                validators = self.custom_validators
                for validator in validators if isinstance(validators, Iterable) else [validators]:
                    validated_values = validator(validated_values)
            except Exception as e:
                raise ValidationError(
                    [ErrorWrapper(e, loc='on operation')],
                    self._ListModel,
                ) from e

        super().__init__(validated_values)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_list

    @classmethod
    def validate_list(cls, value):
        return value if isinstance(value, cls) else cls(value)


@typing.no_type_check
def conlist(item_type: Type[T],
            *,
            min_items: Optional[int] = None,
            max_items: Optional[int] = None,
            custom: Union[ValidationFunc, Iterable[ValidationFunc], None] = None) -> Type[List[T]]:
    """
    Generates a list type with constraints on the length of the list and on the type of items it is allowed to contain.

    This function creates a list type with optional minimum and maximum length constraints. Additionally, it can enforce
    a list to have a specific type of items and also applies custom validation functions.

    :param item_type: The type of items the list should contain.
    :param min_items: The minimum number of items the list should contain. (Default: {py:data}`None`)
    :param max_items: The maximum number of items the list should contain. (Default: {py:data}`None`)
    :param custom: Custom validation functions. This could be a single function or an iterable of functions. (Default:
        {py:data}`None`)
    :return: A list type with the specified constraints.
    """
    namespace = dict(min_items=min_items, max_items=max_items, custom_validators=custom)
    return types.new_class('ConstrainedMutatingListValue', (ConstrainedMutatingList[item_type],), {},
                           lambda ns: ns.update(namespace))
