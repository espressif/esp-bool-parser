# SPDX-FileCopyrightText: 2024-2026 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0

import importlib
import sys
from unittest.mock import patch

import pytest

import esp_bool_parser.constants


def test_constants_missing_raises_error():
    with patch.dict(sys.modules, {'constants': None}):
        with pytest.raises(ImportError) as excinfo:
            importlib.reload(esp_bool_parser.constants)

        assert 'Cannot find ESP-IDF constants.py module' in str(excinfo.value)
