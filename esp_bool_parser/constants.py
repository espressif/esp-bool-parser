# SPDX-FileCopyrightText: 2022-2025 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0

import importlib
import logging
import os
import re
import sys
import typing as t

from .utils import (
    to_version,
)

LOGGER = logging.getLogger(__name__)

_idf_env = os.getenv('IDF_PATH') or ''
if not _idf_env:
    LOGGER.debug('IDF_PATH environment variable is not set. Setting IDF_PATH to current directory...')
IDF_PATH = os.path.abspath(_idf_env)


_idf_py_actions = os.path.join(IDF_PATH, 'tools', 'idf_py_actions')
sys.path.append(_idf_py_actions)
try:
    _idf_py_constant_py = importlib.import_module('constants')
except ModuleNotFoundError:
    LOGGER.debug(
        'Setting supported/preview targets to empty list... (ESP-IDF constants.py module not found under %s)',
        _idf_py_actions,
    )
    _idf_py_constant_py = object()  # type: ignore
SUPPORTED_TARGETS = getattr(_idf_py_constant_py, 'SUPPORTED_TARGETS', [])
PREVIEW_TARGETS = getattr(_idf_py_constant_py, 'PREVIEW_TARGETS', [])
ALL_TARGETS = SUPPORTED_TARGETS + PREVIEW_TARGETS


def _idf_version_from_cmake() -> t.Tuple[int, int, int]:
    version_path = os.path.join(IDF_PATH, 'tools', 'cmake', 'version.cmake')
    if not os.path.isfile(version_path):
        LOGGER.debug('Setting ESP-IDF version to 1.0.0... (ESP-IDF version.cmake not exists at %s)', version_path)
        return 1, 0, 0

    regex = re.compile(r'^\s*set\s*\(\s*IDF_VERSION_([A-Z]{5})\s+(\d+)')
    ver = {}
    try:
        with open(version_path) as f:
            for line in f:
                m = regex.match(line)

                if m:
                    ver[m.group(1)] = m.group(2)

        return int(ver['MAJOR']), int(ver['MINOR']), int(ver['PATCH'])
    except (KeyError, OSError):
        raise ValueError(f'Cannot find ESP-IDF version in {version_path}')


IDF_VERSION_MAJOR, IDF_VERSION_MINOR, IDF_VERSION_PATCH = _idf_version_from_cmake()
IDF_VERSION = to_version(f'{IDF_VERSION_MAJOR}.{IDF_VERSION_MINOR}.{IDF_VERSION_PATCH}')
