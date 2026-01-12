# SPDX-FileCopyrightText: 2024-2026 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0

import pytest

from esp_bool_parser.soc_header import parse_define


@pytest.mark.parametrize(
    's, res',
    [
        ('#define SOC_FOO        (4)', '4'),
        ('#define SOC_FOO        (-4)', '-4'),
        ('#define SOC_FOO       4', '4'),
        ('#define SOC_FOO     -4', '-4'),
    ],
)
def test_parse_define_int(s, res):
    parse_result = parse_define(s)
    assert parse_result['name'] == 'SOC_FOO'
    assert parse_result['int_value'] == res
