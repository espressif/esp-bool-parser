# SPDX-FileCopyrightText: 2025 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0

import shutil

import pytest


@pytest.mark.skipif(not shutil.which('idf.py'), reason='idf.py not found')
def test_idf_version_keywords_type():
    from esp_bool_parser.constants import (
        IDF_VERSION_MAJOR,
        IDF_VERSION_MINOR,
        IDF_VERSION_PATCH,
    )

    assert isinstance(IDF_VERSION_MAJOR, int)
    assert isinstance(IDF_VERSION_MINOR, int)
    assert isinstance(IDF_VERSION_PATCH, int)
