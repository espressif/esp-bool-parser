# SPDX-FileCopyrightText: 2022-2025 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0

"""Tools for building ESP-IDF related apps."""

__version__ = '0.1.4'

import importlib

from .bool_parser import BoolStmt, parse_bool_expr, register_addition_attribute
from .utils import lazy_load

__getattr__ = lazy_load(
    importlib.import_module(__name__),
    {
        'parse_bool_expr': parse_bool_expr,
        'register_addition_attribute': register_addition_attribute,
        'BoolStmt': BoolStmt,
    },
    {
        'IDF_PATH': '.constants',
        'SUPPORTED_TARGETS': '.constants',
        'PREVIEW_TARGETS': '.constants',
        'ALL_TARGETS': '.constants',
        'IDF_VERSION_MAJOR': '.constants',
        'IDF_VERSION_MINOR': '.constants',
        'IDF_VERSION_PATCH': '.constants',
        'IDF_VERSION': '.constants',
        'SOC_HEADERS': '.soc_header',
    },
)

__all__ = [
    'ALL_TARGETS',
    'IDF_PATH',
    'IDF_VERSION',
    'IDF_VERSION_MAJOR',
    'IDF_VERSION_MINOR',
    'IDF_VERSION_PATCH',
    'PREVIEW_TARGETS',
    'SOC_HEADERS',
    'SUPPORTED_TARGETS',
    'BoolStmt',
    'parse_bool_expr',
    'register_addition_attribute',
]
