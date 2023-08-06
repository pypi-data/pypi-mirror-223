"""
Pydantic-compatible field types for objects that are callable.

This module provides utilities to validate and enforce constraints on Python callable objects. A callable in Python is
any object that can be called like a function. The validation includes checks on the number of parameters and the types
of both these parameters and the return value.
"""

from __future__ import annotations

import inspect
from typing import Any, Callable, Optional, Type, Union, get_type_hints

from pydantic.fields import ModelField

from optool.fields.util import check_only_one_specified, get_type_validator, update_object_schema


class ConstrainedCallable:
    """
    Pydantic-compatible field type for {py:class}`typing.Callable` objects.

    :::{seealso}
    [Pydantic documentation: Custom Data Types](https://docs.pydantic.dev/usage/types/#custom-data-types) and
    {py:class}`pydantic.types.ConstrainedInt` or similar of {py:mod}`pydantic`
    :::
    """

    num_params: Optional[int] = None
    param_types: Optional[tuple[type, ...]]
    return_type: Optional[type] = None

    @classmethod
    def __get_validators__(cls):
        yield get_type_validator(Callable)
        yield cls.validate_number_of_parameters
        yield cls.validate_parameter_types
        yield cls.validate_return_type

    @classmethod
    def __modify_schema__(cls, field_schema, field: Optional[ModelField]):
        update_object_schema(field_schema,
                             num_params=cls.num_params,
                             param_types=cls.param_types,
                             return_type=cls.return_type)

    @classmethod
    def validate_number_of_parameters(cls, val: Callable) -> Callable:
        if cls.num_params is None:
            return val

        arg_spec = cls._check_can_verify_params("number of parameters", cls.num_params, val)
        if len(arg_spec.args) == cls.num_params:
            return val
        raise CallableParameterError(spec="number of parameters", expected=cls.num_params, value=arg_spec)

    @classmethod
    def validate_parameter_types(cls, val: Callable) -> Callable:
        if cls.param_types is None:
            return val

        arg_spec = cls._check_can_verify_params("parameter types", cls.num_params, val)
        if not arg_spec.annotations:
            raise CallableParameterError(spec="parameter types", expected=cls.num_params, value=arg_spec)
        if cls.param_types == tuple(arg_spec.annotations[name] for name in arg_spec.args):
            return val
        raise CallableParameterError(spec="parameter types", expected=cls.param_types, value=arg_spec)

    @classmethod
    def validate_return_type(cls, val: Callable) -> Callable:
        if cls.return_type is None:
            return val

        arg_spec: inspect.FullArgSpec = inspect.getfullargspec(val)
        if 'return' not in arg_spec.annotations:
            raise UnverifiableCallableParameterError(spec="return type", expected=cls.num_params, value=arg_spec)
        if cls.return_type == arg_spec.annotations['return']:
            return val
        raise UnverifiableCallableParameterError(spec="return type", expected=cls.return_type, value=arg_spec)

    @classmethod
    def _check_can_verify_params(cls, spec: str, expected: Optional[int], val: Callable) -> inspect.FullArgSpec:
        arg_spec = inspect.getfullargspec(val)
        if any(isinstance(arg_type, str) for arg_type in arg_spec.annotations.values()):
            # Need to use inspect.get_type_hints() to retrieve the evaluated type annotations
            return arg_spec._replace(annotations=get_type_hints(val))
        if arg_spec.varargs or arg_spec.varkw:
            raise UnverifiableCallableParameterError(spec=spec, expected=expected, value=arg_spec)
        return arg_spec


def concallable(*,
                num_params: Optional[int] = None,
                param_types: Union[type, tuple[type, ...], None] = None,
                return_type: Optional[type] = None) -> Type[Callable]:
    """
    Function to create a constrained callable value.

    The constraints could be the number of parameters, types of parameters, and the return type.

    :param num_params: The number of parameters for the callable. Default is {py:data}`None`.
    :param param_types: The type or types of parameters for the callable. If a single type is specified, it is converted
        into a tuple. Default is {py:data}`None`.
    :param return_type: The return type of the callable. Default is {py:data}`None`.
    :return: A new type that is a subclass of {py:class}`ConstrainedCallable`.
    :raises ValueError: If both `num_params` and `param_types` are specified.

    :::{seealso}
    {py:func}`pydantic.conint`, {py:func}`pydantic.confloat`, etc.
    :::
    """
    check_only_one_specified(num_params, param_types, "Cannot specify both number and types of parameters.")
    if isinstance(param_types, type):
        param_types = (param_types,)
    namespace = dict(num_params=num_params, param_types=param_types, return_type=return_type)
    return type('ConstrainedCallableValue', (ConstrainedCallable,), namespace)


class CallableParameterError(ValueError):
    """
    Raised when the callable parameter does not meet the expectations.

    :param spec: The specification for the callable parameter.
    :param expected: The expected callable parameter.
    :param value: The actual value of the callable parameter.
    """

    def __init__(self, *, spec: str, expected: Any, value: inspect.FullArgSpec) -> None:
        super().__init__(f"expected the {spec} {expected}, but got a value with argument specification {value}")


class UnverifiableCallableParameterError(ValueError):
    """
    Raised when it's not possible to verify the callable parameter.

    :param spec: The specification for the callable parameter.
    :param expected: The expected callable parameter.
    :param value: The actual value of the callable parameter.
    """

    def __init__(self, *, spec: str, expected: Any, value: inspect.FullArgSpec) -> None:
        super().__init__(f"cannot verify the callable with argument specification {value} "
                         f"for expected {spec} {expected}")
