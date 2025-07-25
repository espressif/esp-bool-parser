# SPDX-FileCopyrightText: 2022-2025 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0
import operator
import os
import typing as t
from ast import (
    literal_eval,
)
from functools import lru_cache

from packaging.version import (
    Version,
)
from pyparsing import (
    Keyword,
    Literal,
    ParseResults,
    QuotedString,
    Suppress,
    Word,
    alphas,
    delimitedList,
    hexnums,
    infixNotation,
    nums,
    opAssoc,
)

from .utils import (
    InvalidInput,
    to_version,
)


class Stmt:
    """Statement"""

    def get_value(self, target: str, config_name: str) -> t.Any:
        """Lazy calculated. All subclasses of `Stmt` should implement this function.

        :param target: ESP-IDF target
        :param config_name: config name

        :returns: the value of the statement
        """
        raise NotImplementedError('Please implement this function in sub classes')


class ChipAttr(Stmt):
    """Attributes defined in SOC Header Files and other keywords as followed:

    - IDF_TARGET: target
    - INCLUDE_DEFAULT: take the default build targets into account or not
    - IDF_VERSION_MAJOR: major version of ESP-IDF
    - IDF_VERSION_MINOR: minor version of ESP-IDF
    - IDF_VERSION_PATCH: patch version of ESP-IDF
    - CONFIG_NAME: config name defined in the config rules
    """

    addition_attr: t.ClassVar[t.Dict[str, t.Callable]] = {}

    def __init__(self, t: ParseResults):
        self.attr: str = t[0]

    @lru_cache(None)
    def get_value(self, target: str, config_name: str) -> t.Any:
        if self.attr in self.addition_attr:
            return self.addition_attr[self.attr](target=target, config_name=config_name)

        if self.attr == 'IDF_TARGET':
            return target

        if self.attr == 'CONFIG_NAME':
            return config_name

        if self.attr in os.environ:
            return os.environ[self.attr]

        from .constants import (
            IDF_VERSION,
            IDF_VERSION_MAJOR,
            IDF_VERSION_MINOR,
            IDF_VERSION_PATCH,
        )

        if self.attr == 'IDF_VERSION':
            return IDF_VERSION

        if self.attr == 'IDF_VERSION_MAJOR':
            return IDF_VERSION_MAJOR

        if self.attr == 'IDF_VERSION_MINOR':
            return IDF_VERSION_MINOR

        if self.attr == 'IDF_VERSION_PATCH':
            return IDF_VERSION_PATCH

        from .soc_header import SOC_HEADERS

        if self.attr in SOC_HEADERS[target]:
            return SOC_HEADERS[target][self.attr]

        return 0  # default return 0 as false


class Integer(Stmt):
    def __init__(self, t: ParseResults):
        self.expr: str = t[0]

    @lru_cache(None)
    def get_value(self, target: str, config_name: str) -> t.Any:  # noqa: ARG002
        return literal_eval(self.expr)


class String(Stmt):
    def __init__(self, t: ParseResults):
        self.expr: str = t[0]

    @lru_cache(None)
    def get_value(self, target: str, config_name: str) -> t.Any:  # noqa: ARG002
        return literal_eval(f'"{self.expr}"')  # double quotes is swallowed by QuotedString


class List_(Stmt):
    def __init__(self, t: ParseResults):
        self.expr = t

    @lru_cache(None)
    def get_value(self, target: str, config_name: str) -> t.Any:
        return [item.get_value(target, config_name) for item in self.expr]


class BoolStmt(Stmt):
    _OP_DICT: t.ClassVar[t.Dict[str, t.Callable[..., bool]]] = {
        '==': operator.eq,
        '!=': operator.ne,
        '>': operator.gt,
        '>=': operator.ge,
        '<': operator.lt,
        '<=': operator.le,
        'not in': lambda x, y: x not in y,
        'in': lambda x, y: x in y,
    }

    def __init__(self, t: ParseResults):
        self.left: Stmt = t[0]
        self.comparison: str = t[1]
        self.right: Stmt = t[2]

    @lru_cache(None)
    def get_value(self, target: str, config_name: str) -> t.Any:
        _l = self.left.get_value(target, config_name)
        _r = self.right.get_value(target, config_name)

        if self.comparison not in ['in', 'not in']:
            # will use version comparison if any of the operands is a Version
            if any(isinstance(x, Version) for x in [_l, _r]):
                _l = to_version(_l)
                _r = to_version(_r)
        else:
            # use str for "in" and "not in" operator
            if isinstance(_l, Version):
                _l = str(_l)
            if isinstance(_r, Version):
                _r = str(_r)

        if self.comparison in self._OP_DICT:
            return self._OP_DICT[self.comparison](_l, _r)

        raise InvalidInput(f'Unsupported comparison operator: "{self.comparison}"')


class BoolExpr(Stmt):
    pass


def _and(_l, _r):
    return _l and _r


def _or(_l, _r):
    return _l or _r


class BoolOr(BoolExpr):
    def __init__(self, res: ParseResults):
        self.bool_stmts: t.List[BoolStmt] = [stmt for stmt in res[0] if stmt != 'or']

    @lru_cache(None)
    def get_value(self, target: str, config_name: str) -> t.Any:
        return any(stmt.get_value(target, config_name) for stmt in self.bool_stmts)


class BoolAnd(BoolExpr):
    def __init__(self, res: ParseResults):
        self.bool_stmts: t.List[BoolStmt] = [stmt for stmt in res[0] if stmt != 'and']

    @lru_cache(None)
    def get_value(self, target: str, config_name: str) -> t.Any:
        return all(stmt.get_value(target, config_name) for stmt in self.bool_stmts)


CAP_WORD = Word(alphas.upper(), nums + alphas.upper() + '_').setParseAction(ChipAttr)

DECIMAL_NUMBER = Word(nums)
HEX_NUMBER = Literal('0x') + Word(hexnums)
INTEGER = (HEX_NUMBER | DECIMAL_NUMBER).setParseAction(Integer)

STRING = QuotedString('"').setParseAction(String)

LIST = Suppress('[') + delimitedList(INTEGER | STRING).setParseAction(List_) + Suppress(']')

BOOL_OPERAND = CAP_WORD | INTEGER | STRING | LIST

EQ = Keyword('==').setParseAction(lambda t: t[0])
NE = Keyword('!=').setParseAction(lambda t: t[0])
LE = Keyword('<=').setParseAction(lambda t: t[0])
LT = Keyword('<').setParseAction(lambda t: t[0])
GE = Keyword('>=').setParseAction(lambda t: t[0])
GT = Keyword('>').setParseAction(lambda t: t[0])
NOT_IN = Keyword('not in').setParseAction(lambda t: t[0])
IN = Keyword('in').setParseAction(lambda t: t[0])

BOOL_STMT = BOOL_OPERAND + (EQ | NE | LE | LT | GE | GT | NOT_IN | IN) + BOOL_OPERAND
BOOL_STMT.setParseAction(BoolStmt)

AND = Keyword('and')
OR = Keyword('or')

BOOL_EXPR = infixNotation(
    BOOL_STMT,
    [
        (AND, 2, opAssoc.LEFT, BoolAnd),
        (OR, 2, opAssoc.LEFT, BoolOr),
    ],
)


def register_addition_attribute(attr: str, action: t.Callable[..., t.Any]) -> None:
    """Register an additional attribute for ChipAttr.

    :param attr: The name of the additional attribute (string).
    :param action: A callable that processes ``**kwargs``. The ``target`` and
        ``config_name`` parameters will be passed as kwargs when the attribute is
        detected.
    """
    ChipAttr.addition_attr[attr] = action


def parse_bool_expr(stmt: str) -> BoolStmt:
    """Parse a boolean expression.

    :param stmt: A string containing the boolean expression.

    :returns: A ``BoolStmt`` object representing the parsed expression.

    .. note::

        You can use this function to parse a boolean expression and evaluate its value
        based on the given context. For example:

        .. code-block:: python

            stmt_string = 'IDF_TARGET == "esp32"'
            stmt: BoolStmt = parse_bool_expr(stmt_string)
            value = stmt.get_value("esp32", "config_name")
            print(value)
            # Output: True
    """
    return BOOL_EXPR.parseString(stmt)[0]
