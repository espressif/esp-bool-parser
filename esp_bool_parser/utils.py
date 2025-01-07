# SPDX-FileCopyrightText: 2025 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0

import importlib
import typing as t

from packaging.version import (
    Version,
)

_ModuleType: t.Any = type(importlib)


def lazy_load(
    base_module: _ModuleType, name_obj_dict: t.Dict[str, t.Any], obj_module_dict: t.Dict[str, str]
) -> t.Callable[[str], t.Any]:
    """
    use __getattr__ in the __init__.py file to lazy load some objects

    Args:
        base_module (ModuleType): base package module
        name_obj_dict (dict[str, any]): name, real object dict, used to store real objects,
            no need to add lazy-load objects
        obj_module_dict (dict[str, str]): dict of object name and module name

    Returns:
        __getattr__ function

    Example:

        ::

            __getattr__ = lazy_load(
                importlib.import_module(__name__),
                {
                    'IdfApp': IdfApp,
                    'LinuxDut': LinuxDut,
                    'LinuxSerial': LinuxSerial,
                    'CaseTester': CaseTester,
                },
                {
                    'IdfSerial': '.serial',
                    'IdfDut': '.dut',
                },
            )
    """

    def __getattr__(object_name):
        if object_name in name_obj_dict:
            return name_obj_dict[object_name]
        elif object_name in obj_module_dict:
            module = importlib.import_module(obj_module_dict[object_name], base_module.__name__)
            imported = getattr(module, object_name)
            name_obj_dict[object_name] = imported
            return imported
        else:
            raise AttributeError('Attribute %s not found in module %s', object_name, base_module.__name__)

    return __getattr__


class InvalidInput(SystemExit):
    """Invalid input from user"""


class InvalidIfClause(SystemExit):
    """Invalid if clause in manifest file"""


def to_version(s: t.Any) -> Version:
    if isinstance(s, Version):
        return s

    try:
        return Version(str(s))
    except ValueError:
        raise InvalidInput(f'Invalid version: {s}')
