"""
Representation of optimization problem that can be defined and solved without the need for cumbersome notation.

This module is a provides the core implementation for formulating optimization problems and managing their components.
It provides a consistent framework to encapsulate problem elements, promoting efficient organization and manipulation of
complex problem structures, thereby simplifying the optimization process.
"""

import io
import re
from abc import ABC, abstractmethod
from contextlib import redirect_stdout
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Type, TypeVar, Union, final

import casadi
import numpy as np
from pydantic import StrictFloat, StrictInt, StrictStr, validate_arguments, validator

from optool.core import BaseModel
from optool.fields.containers import ConstrainedMutatingList
from optool.fields.numeric import ImmutableArray
from optool.fields.quantities import QuantityLike, UnitLike
from optool.fields.symbolic import CasadiColumn, CasadiScalar
from optool.fields.util import validate, validate_each
from optool.logging import LOGGER
from optool.math import is_symbolic, num_elements
from optool.optimization.constraints import BoxConstraint, Equation, ExpressionConstraint, OptimizationConstraint
from optool.optimization.helpers import DebugInfo, IpoptOption, SolverResponse
from optool.optimization.variables import CasadiVariable, OptimizationVariable
from optool.uom import UNITS, Quantity, Unit
from optool.util import ValueRange


@validate_arguments
def _find_element(name: str, elements: list[Any]) -> Optional[int]:
    """
    Finds the index at which the element with the specified name is located in the specified list of elements.

    :param name: The name of the variable or constraint.
    :param elements: The list of elements to search.
    :returns: The index at which the element is located, or {py:data}`None` if the element is not present in the list.
    """

    validate_each(elements, lambda x: hasattr(x, "name"), "Element is missing attribute 'name', see {value}.")
    index = [i for (i, element) in enumerate(elements) if name == element.name]
    if not index:
        return None
    if len(index) == 1:
        return index[0]

    if isinstance(elements[0], OptimizationVariable):
        element_type = "variable"
    elif isinstance(elements[0], OptimizationConstraint):
        element_type = "constraint"
    else:
        element_type = elements[0].__class__.__name__
    raise ValueError(f"There should be at most one {element_type} entitled '{name}', but found {len(index)}.")


def _get_dummy_solver(formulation, inputs):
    if formulation == "NLP":
        return casadi.nlpsol(*inputs)
    elif formulation == "QP":
        return casadi.qpsol(*inputs)
    else:
        raise ValueError(f"Unknown type '{formulation}'. Use either 'NLP' or 'QP'.")


if TYPE_CHECKING:
    VariableList = list
    ConstraintList = list
else:

    def _is_distinct(_, values):  # First parameter is the ConstrainedMutatingList itself
        """
        Validates if all elements in the list have distinct names.

        :param values: A list of elements.
        :return: The input list if validation is successful.
        """
        names = [element.name for element in values]
        validate(names, len(names) == len(set(names)), 'All names must be distinct, but have {value}.')
        return values

    class VariableList(ConstrainedMutatingList[OptimizationVariable]):
        """
        List that accepts only elements of type {py:class}`~optool.optimization.variables.OptimizationVariable`, the
        names of which must be distinct.
        """
        custom_validators = _is_distinct

    class ConstraintList(ConstrainedMutatingList[OptimizationConstraint]):
        """
        List that accepts only elements of type {py:class}`~optool.optimization.constraints.OptimizationConstraint`, the
        names of which must be distinct.
        """
        custom_validators = _is_distinct


class ProblemElements(BaseModel):
    """
    Container for storing and managing the variables and constraints of an optimization problem.

    :param variables: A list of variables of the optimization problem.
    :param constraints: A list of constraints of the optimization problem.
    """

    variables: VariableList = []
    """A list of variables of the optimization problem."""
    constraints: ConstraintList = []
    """A list of constraints of the optimization problem."""

    def has_variable(self, name: str) -> bool:
        """
        Checks if a variable with the specified name exists in the problem.

        :param name: Name of the variable.
        :return: {py:data}`True` if variable exists, {py:data}`False` otherwise.
        """
        return _find_element(name, self.variables) is not None

    def get_variable(self, name: str) -> OptimizationVariable:
        """
        Retrieves a variable by its name.

        :param name: Name of the variable.
        :return: The variable with the specified name.
        :raises ValueError: If no variable with the specified name is found.
        """
        index = _find_element(name, self.variables)
        if index is None:
            raise ValueError(f"The variable {name!r} is not present. Here is a list of all available variables:"
                             f"\n{[var.name for var in self.variables]}")
        return self.variables[index]

    def has_constraint(self, name: str) -> bool:
        """
        Checks if a constraint with the specified name exists in the problem.

        :param name: Name of the constraint.
        :return: {py:data}`True` if constraint exists, {py:data}`False` otherwise
        """

        return _find_element(name, self.constraints) is not None

    def get_constraint(self, name: str) -> OptimizationConstraint:
        """
        Retrieves a constraint by its name.

        :param name: Name of the constraint.
        :return: The constraint with the specified name.
        :raises ValueError: If no constraint with the specified name is found.
        """
        index = _find_element(name, self.constraints)
        if index is None:
            raise ValueError(f"The constraint {name!r} is not present. Here is a list of all available constraints:"
                             f"\n{[var.name for var in self.constraints]}")
        return self.constraints[index]


class OptimizationProblem(ProblemElements, ABC):  # Abstract base class
    """
    Definition of an optimization program.

    Convenient interface to define and solve an optimization problem without the need for cumbersome notation.
    """

    name: StrictStr = ""
    """The name of the optimization problem."""

    @abstractmethod
    def parse(self, solver: str, options: Dict[str, Any]) -> None:
        """
        Parses the problem as specified such that it can be solved afterward.

        :param solver: A solver specified as string, e.g., `ipopt`.
        :param options: A Dictionary of options.

        :::{admonition} Example
        :class: example

        ```python
        obj.parse('ipopt')
        ```
        """
        raise NotImplementedError()

    @abstractmethod
    def solve(self) -> SolverResponse:
        """
        Solves the formulated optimization problem.

        Solves the optimization problem and writes the results into the solution fields of the optimization variables.

        :::{admonition} Example
        :class: example

        ```python
        status = obj.solve()
        ```
        """
        raise NotImplementedError()

    @staticmethod
    def casadi(name=""):
        return CasadiProblem(name=name)

    @abstractmethod
    def new_variable(self, name: str, n: int, unit: Optional[Unit] = None) -> OptimizationVariable:
        """
        Creates and adds a new optimization variable to the optimization problem.

        :param name: Name of the new variable.
        :param n: Number of elements of the new variable.
        :param unit: Physical unit of the new variable.
        :return: The variable created.
        """
        raise NotImplementedError()

    @abstractmethod
    def add_equality_constraint(self, lhs, rhs, nominal_value=None) -> OptimizationConstraint:
        """
        Adds an equality constraint forcing the left-hand side (lhs) to be equal to the right-hand side (rhs).

        :param lhs: Left-hand side expression.
        :param rhs: Right-hand side expression.
        :param nominal_value: The nominal value to be used for the equality constraint.
        :return: The constraint added.
        """
        raise NotImplementedError()

    @abstractmethod
    def add_box_constraint(self, lower_bound, expression, upper_bound, nominal_value=None) -> OptimizationConstraint:
        """
        Adds a box constraint that forces the expression to be within (or equal to) the bounds specified.

        :param lower_bound: The lower bound for the box constraint.
        :param expression: The expression to be constrained.
        :param upper_bound: The upper bound for the box constraint.
        :param nominal_value: The nominal value to be used for the box constraint.
        :return: The constraint added.
        """
        raise NotImplementedError()

    @abstractmethod
    def add_greater_than_constraint(self, lower_bound, expression, nominal_value=None) -> OptimizationConstraint:
        """
        Adds a constraint that forces the expression to be greater than or equal to a lower bound.

        :param lower_bound: The lower bound for the constraint.
        :param expression: The expression to be constrained.
        :param nominal_value: The nominal value to be used for the constraint.
        :return: The constraint added.
        """
        raise NotImplementedError()

    @abstractmethod
    def add_less_than_constraint(self, expression, upper_bound, nominal_value=None) -> OptimizationConstraint:
        """
        Adds a constraint that forces the expression to be smaller than or equal to a lower bound.

        :param expression: The expression to be constrained.
        :param upper_bound: The upper bound for the constraint.
        :param nominal_value: The nominal value to be used for the constraint.
        :return: The added constraint.
        """
        raise NotImplementedError()

    @abstractmethod
    def add_equation(self, equation: Equation) -> BoxConstraint:
        """
        Adds an equation that describes the equality of two expressions.

        :param equation: The equation to add.
        :return: The added constraint.
        """
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def get_parser_options(formulation: str = "NLP", solver: str = "ipopt") -> Dict[str, Tuple[str, str]]:
        """
        Retrieves the solver options for a given solver and formulation.

        :param formulation: The formulation for which to retrieve the options.
        :param solver: The solver for which to retrieve the options.
        :return: A dictionary describing the available parser options.
        """
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def get_solver_options(formulation: str = "NLP", solver: str = "ipopt") -> frozenset[IpoptOption]:
        """
        Retrieves the parser options for a given solver and formulation.

        :param formulation: The formulation for which to retrieve the options.
        :param solver: The solver for which to retrieve the options.
        :return: A set of the available solver options.
        """
        raise NotImplementedError()


# noinspection PyArgumentList
def robust_divide_units(numerator: Optional[Unit], denominator: Optional[Unit]) -> Optional[Unit]:
    """
    Performs division between two units in a way that tolerates {py:data}`None` values.

    :param numerator: The numerator unit.
    :param denominator: The denominator unit.
    :return: The result of division, if applicable. If both numerator and denominator are {py:data}`None`, returns
    {py:data}`None`.
    """
    if numerator is None and denominator is None:
        return None
    elif numerator is None:
        return 1 / denominator  # type: ignore
    elif denominator is None:
        return numerator
    return numerator / denominator


_T = TypeVar("_T", bound=OptimizationConstraint)


class CasadiProblem(OptimizationProblem):
    """Representation of an optimization problem using the modeling language [CasADi](https://web.casadi.org)."""

    _solver: casadi.Function = None

    objective: Optional[QuantityLike[Any, CasadiScalar]] = None
    """The objective to minimize."""

    @final
    @validator('constraints')
    def _is_supported_constraint(cls, value):
        types = [type(element) for element in value]
        for element in value:
            validate(element, lambda x: isinstance(x, BoxConstraint),
                     f"All constraints of {cls.__name__} must be {BoxConstraint.__name__}, but have {types}.")
        return value

    def parse(self, solver: str, options=None) -> None:
        if options is None:
            options = {}
        if self._solver is not None:
            raise ValueError("The problem has already been parsed.")

        LOGGER.info("Parsing the problem entitled {!r}", self.name)

        if unnamed_constraints := [val for val in self._get_constraints(OptimizationConstraint) if val.name == ""]:
            LOGGER.debug("There are {} unnamed constraints that are automatically named now.", len(unnamed_constraints))
            for i, val in enumerate(unnamed_constraints):
                val.name = f"(unnamed constraint {i})"

        g_constraints = self._get_constraints(BoxConstraint)
        h_constraints = self._get_constraints(ExpressionConstraint)

        LOGGER.debug("Assembling {} variables with following names and sizes: {}.", len(self.variables),
                     [(val.name, val.length()) for val in self.variables])
        LOGGER.debug("Assembling the following {} constraints: {}.", len(self.constraints),
                     [f"{val.__class__.__name__}({val.name})" for val in self.constraints])

        # Assemble problem definition
        problem = {
            'x': casadi.vertcat(*[val.normed for val in self.variables]),
            'g': casadi.vertcat(*[val.get_symbols() for val in g_constraints]),
            # 'h': casadi.diagcat(*h_constraints)
        }
        if self.objective is not None:
            problem['f'] = self.objective.magnitude

        # problem.p = vertcat(optParameters.regularVariable);

        # Create solver object
        solver_type = casadi.qpsol if h_constraints else casadi.nlpsol
        self._solver = solver_type("solver", solver, problem, options)

        LOGGER.info("Finished parsing the problem {!r}.", self.name)

    def solve(self) -> SolverResponse:
        if not self._solver:
            ValueError(f"The problem entitled {self.name!r} needs to be parsed first.")

        # Assemble problem definition
        inputs = {
            "x0": self._get_normed_replicated_variable_values('initial_guess'),
            "lbx": self._get_normed_replicated_variable_values('lower_bounds'),
            "ubx": self._get_normed_replicated_variable_values('upper_bounds'),
            "lbg": self._get_normed_replicated_constraint_bounds("get_dimensionless_lower_bound"),
            "ubg": self._get_normed_replicated_constraint_bounds("get_dimensionless_upper_bound")
        }

        # Constraints
        # inputs["p"] = vertcat(optParameters.value)

        # Solve the NLP
        LOGGER.info("Solving the optimization problem entitled {!r}.", self.name)
        sol = self._solver(**inputs)
        status = self._solver.stats()
        debug_info = DebugInfo(problem_name=self.name)
        LOGGER.debug("Solver return status: {}", status["return_status"])
        LOGGER.debug("Solver iteration count: {}", status["iter_count"])
        LOGGER.info("Solved optimization problem entitled {!r}.", self.name)

        # Get Solution
        if self.objective is not None:
            unit_of_objective = self.objective.units
            function_value = Quantity(float(sol["f"].full()), unit_of_objective)
        else:
            unit_of_objective = UNITS.one
            function_value = None

        # Variables
        end_split_indices = np.cumsum([val.length() for val in self.variables])
        normed_values = np.split(sol["x"].full().squeeze(), end_split_indices)
        # lagrange_multipliers = np.split(sol["lam_x"].full().squeeze(), end_split_indices)

        for i, val in enumerate(self.variables):
            val.solution = normed_values[i] * val.nominal_values
            # val.lagrange_multipliers = lagrange_multipliers[i]
            debug_info.normed_variable_values.append(ValueRange.of(val.name, normed_values[i]))

        # Box constraints
        box_constraints = self._get_constraints(BoxConstraint)
        constraint_lengths = [val.length() for val in box_constraints]
        end_split_indices = np.cumsum(constraint_lengths)
        lagrange_multipliers = np.split(sol["lam_g"].full().squeeze(), end_split_indices)

        for i, val in enumerate(box_constraints):
            lagrange_multipliers_unit = robust_divide_units(unit_of_objective, val.get_unit())
            val.lagrange_multipliers = Quantity(lagrange_multipliers[i] / val.nominal_value, lagrange_multipliers_unit)
            debug_info.normed_constraints_lagrange_multipliers.append(ValueRange.of(val.name, lagrange_multipliers[i]))

        # Parameters
        # end_split_indices = np.cumsum([val.length() for val in obj.parameters])
        # lagrange_multipliers = np.split(sol["lam_p"].full().squeeze(), end_split_indices)
        # for i, val in enumerate(obj.parameters):
        #     val.lagrange_multipliers = lagrange_multipliers[i]

        return SolverResponse(problem_name=self.name,
                              function_value=function_value,
                              success=status["success"],
                              solver_status=status,
                              debug_info=debug_info)

    def _get_constraints(self, constraint_type: Type[_T]) -> List[_T]:
        return list(filter(lambda x: isinstance(x, constraint_type), self.constraints))

    def _get_normed_replicated_variable_values(self, field_name: str) -> np.ndarray:
        normed_values = [getattr(val, field_name) / val.nominal_values for val in self.variables]
        dimensionless_values = [val.m_as(UNITS.dimensionless) for val in normed_values]
        return np.concatenate(dimensionless_values)

    def _get_normed_replicated_constraint_bounds(self, method_name: str):
        box_constraints = self._get_constraints(BoxConstraint)
        dimensionless_values = [getattr(val, method_name)() for val in box_constraints]
        return np.concatenate(dimensionless_values)

    @validate_arguments
    def new_variable(self, name: StrictStr, n: StrictInt, unit: Optional[UnitLike] = None) -> CasadiVariable:
        variable = OptimizationVariable.casadi(name, n, unit)
        self.variables.append(variable)
        return variable

    @validate_arguments
    def add_equality_constraint(self,
                                lhs: QuantityLike[Any, Union[ImmutableArray, CasadiColumn]],
                                rhs: QuantityLike[Any, Union[ImmutableArray, CasadiColumn]],
                                nominal_value: StrictFloat = 1.0) -> BoxConstraint:

        if num_elements(lhs) != num_elements(rhs):
            raise ValueError(f"The number of values on the right-hand side and on the left-hand side must be equal, "
                             f"but have {num_elements(lhs)} and {num_elements(rhs)}, respectively.")

        difference = lhs - rhs
        zero = Quantity(0.0, difference.units)
        constraint = BoxConstraint(name=f"constraint-{len(self.constraints)}",
                                   lower_bound=zero,
                                   expression=difference / nominal_value,
                                   upper_bound=zero,
                                   nominal_value=nominal_value)
        self.constraints.append(constraint)
        return constraint

    @validate_arguments
    def add_box_constraint(self,
                           lower_bound: QuantityLike[Any, Union[float, ImmutableArray]],
                           expression: QuantityLike[Any, Union[ImmutableArray, CasadiColumn]],
                           upper_bound: QuantityLike[Any, Union[float, ImmutableArray]],
                           nominal_value: StrictFloat = 1.0) -> BoxConstraint:

        expression_length = num_elements(expression)
        if any(num_elements(bound) not in [1, expression_length] for bound in [lower_bound, upper_bound]):
            raise ValueError(f"The number of values of the lower bound, the value, and the upper bound are not equal, "
                             f"but have {num_elements(lower_bound)}, {num_elements(expression)}, "
                             f"and {num_elements(upper_bound)}, respectively.")

        constraint = BoxConstraint(name=f"constraint-{len(self.constraints)}",
                                   lower_bound=lower_bound / nominal_value,
                                   expression=expression / nominal_value,
                                   upper_bound=upper_bound / nominal_value,
                                   nominal_value=nominal_value)
        self.constraints.append(constraint)
        return constraint

    @validate_arguments
    def add_greater_than_constraint(self,
                                    lower_bound: QuantityLike[Any, Union[ImmutableArray, CasadiColumn]],
                                    expression: QuantityLike[Any, Union[ImmutableArray, CasadiColumn]],
                                    nominal_value: StrictFloat = 1.0) -> BoxConstraint:

        if is_symbolic(lower_bound):
            expression = expression - lower_bound
            lower_bound = Quantity(0.0, expression.units)
        constraint = BoxConstraint(name=f"constraint-{len(self.constraints)}",
                                   lower_bound=lower_bound / nominal_value,
                                   expression=expression / nominal_value,
                                   upper_bound=None,
                                   nominal_value=nominal_value)
        self.constraints.append(constraint)
        return constraint

    @validate_arguments
    def add_less_than_constraint(self,
                                 expression: QuantityLike[Any, Union[ImmutableArray, CasadiColumn]],
                                 upper_bound: QuantityLike[Any, Union[ImmutableArray, CasadiColumn]],
                                 nominal_value: StrictFloat = 1.0) -> BoxConstraint:

        if is_symbolic(upper_bound):
            expression = expression - upper_bound
            upper_bound = Quantity(0.0, expression.units)
        constraint = BoxConstraint(name=f"constraint-{len(self.constraints)}",
                                   lower_bound=None,
                                   expression=expression / nominal_value,
                                   upper_bound=upper_bound / nominal_value,
                                   nominal_value=nominal_value)
        self.constraints.append(constraint)
        return constraint

    @validate_arguments
    def add_equation(self, equation: Equation) -> BoxConstraint:
        constraint = self.add_equality_constraint(equation.lhs, equation.rhs)
        constraint.name = equation.name
        return constraint

    @staticmethod
    def get_parser_options(formulation: str = "NLP", solver: str = "ipopt") -> Dict[str, Tuple[str, str]]:
        inputs = ("solver", solver, {'x': casadi.SX.sym("", 1, 1)})
        dummy_solver = _get_dummy_solver(formulation, inputs)

        output = io.StringIO()
        with redirect_stdout(output):
            dummy_solver.print_options()
        option_details = output.getvalue().splitlines()[1:]

        options = {}
        for line in option_details:
            if len(line) > 0:
                var_type = re.findall(r"(?<=\[).*?(?=\])", line)[0]  # not greedy search
                [option_name, description] = line.split(var_type)
                option_name = re.findall(r"(?<=\").*(?=\")", option_name)[0]  # greedy search
                description = re.findall(r"(?<=\").*(?=\")", description)[0]  # greedy search
                options[option_name] = (var_type, description)

        return options

    @staticmethod
    def get_solver_options(formulation: str = "NLP", solver: str = "ipopt") -> frozenset[IpoptOption]:
        if solver == "ipopt":
            solver_opts = {"ipopt.print_options_documentation": "yes"}
        else:
            raise ValueError(f"Unknown solver '{solver}'. Currently only 'ipopt' is supported.")

        inputs = ("solver", solver, {'x': casadi.SX.sym("", 1, 1)}, solver_opts)

        output = io.StringIO()
        with redirect_stdout(output):
            _get_dummy_solver(formulation, inputs)
        option_details = output.getvalue().splitlines()

        options: list[IpoptOption] = []
        category = None
        option_name = None
        option_values = None
        description: List[str] = []
        for line in option_details:
            if len(line.strip()) == 0:
                continue
            elif line.startswith("###"):
                category = re.findall(r"(?<=### ).*(?= ###)", line)[0]
            elif not line.startswith(" "):
                option_header = re.findall(r"^\w+", line)
                if option_name is not None and option_name != option_header[0]:
                    options.append(
                        IpoptOption(category=category,
                                    name=option_name,
                                    values=option_values,
                                    description="\n".join(description)))
                option_name = option_header[0]
                option_values = line.replace(option_name, "").strip()
                description = []
            else:
                description.append(line)

        return frozenset(options)
