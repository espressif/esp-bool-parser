# SPDX-FileCopyrightText: 2025-2026 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0


def test_load():
    import esp_bool_parser

    for el in esp_bool_parser.__all__:
        esp_bool_parser.__getattr__(el)
