# SPDX-FileCopyrightText: 2024-2026 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0

import sys
from unittest.mock import MagicMock

# Mock ESP-IDF constants
mock_idf_constants = MagicMock()
mock_idf_constants.SUPPORTED_TARGETS = [
    'esp32',
    'esp32s2',
    'esp32s3',
    'esp32c3',
    'esp32c2',
    'esp32c6',
    'esp32h2',
    'esp32p4',
]
mock_idf_constants.PREVIEW_TARGETS = []
sys.modules['constants'] = mock_idf_constants
