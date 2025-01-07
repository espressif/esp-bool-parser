# SPDX-FileCopyrightText: 2022-2025 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0

"""
Tools for building ESP-IDF related apps.
"""

# ruff: noqa: E402

__version__ = '0.1.1'

from .bool_parser import parse_bool_expr, register_addition_attribute

__all__ = [
    'parse_bool_expr',
    'register_addition_attribute',
]
