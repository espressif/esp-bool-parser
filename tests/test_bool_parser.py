# SPDX-FileCopyrightText: 2024-2026 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0

import pytest

import esp_bool_parser.constants
from esp_bool_parser.bool_parser import parse_bool_expr, register_addition_attribute
from esp_bool_parser.utils import to_version


@pytest.mark.parametrize(
    's, res',
    [
        ('1 == 1', True),
        ('"a" == "a"', True),
        ('1 == 2', False),
        ('"a" == "b"', False),
    ],
)
def test_simple_parse(s, res):
    stmt = parse_bool_expr(s)
    result = stmt.get_value('', '')
    assert result == res


@pytest.mark.parametrize(
    's, res',
    [
        ('SOMETHING == 2', True),
        ('SOMETHING == 1', False),
    ],
)
def test_extend_attr(s, res):
    stmt = parse_bool_expr(s)

    def _process_attr(**kwargs):
        return kwargs.get('target') * 2

    register_addition_attribute('SOMETHING', _process_attr)
    result = stmt.get_value(1, '')
    assert result == res


@pytest.mark.parametrize(
    's, res',
    [
        ('1 == 0 or 2 == 0 or 3 == 3', True),
        ('1 == 0 and 3 == 3', False),
        ('1 == 1 and 2 == 2 or 3 == 0', True),
        ('1 == 1 and 2 == 0 or 3 == 0', False),
        ('1 == 1 and 2 == 2 and 3 == 1', False),
        ('1 == 1 and 2 == 2 and 3 == 3', True),
        ('1 == 1 and 2 == 2 or 3 == 0 and 4 == 0', True),
        ('1 == 1 and 2 == 0 or 3 == 0 and 4 == 0', False),
        ('1 == 1 and 2 == 0 or 3 == 3 and 4 == 4', True),
        ('1 == 1 and 2 == 2 and 3 == 0 or 4 == 4', True),
        ('(1 == 1 and 2 == 2) or 3 == 0', True),
        ('1 == 1 and (2 == 2 or 3 == 3)', True),
        ('1 == 1 and (2 == 0 or 3 == 3)', True),
        ('(1 == 1 and 2 == 2) and (3 == 3 or 4 == 0)', True),
        ('(1 == 1 and 2 == 0) or (3 == 3 and 4 == 4)', True),
        ('(1 == 1 and 2 == 2) or (3 == 3 and 4 == 4)', True),
        ('1 == 1 and (2 == 2 or 3 == 0) and 4 == 4', True),
        ('(1 == 1 or 2 == 0) and (3 == 3 or 4 == 0)', True),
        ('1 == 1 and (2 == 0 or 3 == 3) and (4 == 4 or 5 == 5)', True),
        ('(1 == 1 and 2 == 0) or (3 == 3 and (4 == 4 or 5 == 5))', True),
        ('(1 == 1 and (2 == 2 or 3 == 3)) or (4 == 4 and 5 == 5)', True),
        ('1 == 1 or (2 == 0 and (3 == 3 or 4 == 4))', True),
        ('(1 == 1 or 2 == 2) and (3 == 3 or (4 == 4 and 5 == 5))', True),
        ('1 == 1 or (2 == 2 and (3 == 3 or 4 == 0))', True),
        ('(1 == 1 and (2 == 2 or 3 == 0)) or (4 == 4 and 5 == 5)', True),
        ('(1 == 1 and (2 == 2 or (3 == 3 and 4 == 4))) or 5 == 5', True),
        ('(1 == 1 and 2 == 2) or (3 == 0 and 4 == 4)', True),
        ('1 == 1 and (2 == 2 or 3 == 0) and 4 == 0', False),
        ('(1 == 0 or 2 == 0) and (3 == 0 or 4 == 0)', False),
        ('1 == 0 and (2 == 0 or 3 == 3) and (4 == 4 or 5 == 5)', False),
        ('(1 == 1 and 2 == 2) and (3 == 3 and 4 == 0)', False),
        ('(1 == 1 and 2 == 0) or (3 == 3 and (4 == 0 or 5 == 1))', False),
        ('(1 == 0 and (2 == 2 or 3 == 3)) or (4 == 4 and 5 == 0)', False),
        ('1 == 0 or (2 == 0 and (3 == 3 or 4 == 4))', False),
        ('(1 == 0 or 2 == 0) and (3 == 3 or (4 == 4 and 5 == 5))', False),
        ('1 == 0 or (2 == 0 and (3 == 0 or 4 == 0))', False),
        ('(1 == 0 and (2 == 2 or (3 == 3 and 4 == 4))) or 5 == 0', False),
        ('(1 == 1 and (2 == 0 or (3 == 3 and 4 == 5))) or 5 == 0', False),
        ('(1 == 1 and 2 == 0) or (3 == 0 and (4 == 0 or 5 == 0))', False),
    ],
)
def test_chain_rule(s, res):
    stmt = parse_bool_expr(s)
    result = stmt.get_value('', '')
    assert result == res


def test_idf_version(monkeypatch):
    monkeypatch.setattr(esp_bool_parser.constants, 'IDF_VERSION', to_version('5.9.0'))
    statement = 'IDF_VERSION > "5.10.0"'
    assert parse_bool_expr(statement).get_value('esp32', 'foo') is False

    statement = 'IDF_VERSION < "5.10.0"'
    assert parse_bool_expr(statement).get_value('esp32', 'foo') is True

    statement = 'IDF_VERSION in  ["5.9.0"]'
    assert parse_bool_expr(statement).get_value('esp32', 'foo') is True
