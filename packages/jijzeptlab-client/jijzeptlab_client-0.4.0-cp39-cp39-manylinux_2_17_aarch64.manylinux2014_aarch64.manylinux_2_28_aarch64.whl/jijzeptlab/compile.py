import dataclasses
import typing as typ

import jijmodeling as jm
import jijmodeling_transpiler as jmt
from jijzeptlab.utils.jijmodeling import INSTANCE_DATA_INTERFACE, FIXED_VARS_INTERFACE

from jijzeptlab.jijzeptlab import (
    FixedVariables as FixedVariables,
    InstanceData as InstanceData,
)
from jijzeptlab.utils.baseclass import Option as Option


class CompileOption(Option):
    """Compile option

    Attributes:
        needs_normalize (bool): Whether to normalize the problem. Defaults to False.
    """

    needs_normalize: bool = False


class CompiledInstance:
    """Compiled instance

    Attributes:
        compile_option (CompileOption): Compile option
        problem (jm.Problem): Problem
        instance_data (InstanceData): Instance data
        fixed_variables (FixedVariables): Fixed variables
    """

    compile_option: CompileOption
    problem: jm.Problem
    instance_data: InstanceData
    fixed_variables: FixedVariables

    def __init__(
        self,
        engine_instance,
        compile_option: CompileOption,
        problem: jm.Problem,
        instance_data: InstanceData,
        fixed_variables: FixedVariables,
    ) -> None:
        self._instance = engine_instance
        self.compile_option = compile_option
        self.problem = problem
        self.instance_data = instance_data
        self.fixed_variables = fixed_variables

    def append_constraint(
        self,
        constraint: jm.Constraint,
        instance_data: typ.Union[InstanceData, INSTANCE_DATA_INTERFACE],
    ):
        pass


def compile_model(
    problem: jm.Problem,
    instance_data: typ.Union[InstanceData, INSTANCE_DATA_INTERFACE],
    fixed_variables: typ.Optional[
        typ.Union[FixedVariables, FIXED_VARS_INTERFACE]
    ] = None,
    option: typ.Optional[CompileOption] = None,
) -> CompiledInstance:
    """Compile a problem

    Args:
        problem (jm.Problem): Problem to be compiled
        instance_data (InstanceData): Instance data
        fixed_variables (FixedVariables, optional): Fixed variables. Defaults to None.
        option (CompileOption, optional): Compile option. Defaults to None.

    Returns:
        CompiledInstance: Compiled instance
    """

    from jijzeptlab.process.process import BackendProcess

    _option: CompileOption
    if option is not None:
        _option = option
    else:
        _option = CompileOption()

    _fixed_vars: FixedVariables
    if fixed_variables is None:
        _fixed_vars = FixedVariables()
    elif isinstance(fixed_variables, dict):  # FIXED_VARS_INTERFACE
        _fixed_vars = FixedVariables.from_dict(fixed_variables)
    else:
        _fixed_vars = fixed_variables

    _instance_data: InstanceData
    if isinstance(instance_data, dict):  # INSTANCE_DATA_INTERFACE
        _instance_data = InstanceData.from_dict(instance_data)
    else:
        _instance_data = instance_data

    return BackendProcess.compile_model(problem, _instance_data, _fixed_vars, _option)
