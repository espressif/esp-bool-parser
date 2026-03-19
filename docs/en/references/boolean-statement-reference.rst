#############################
 Boolean Statement Reference
#############################

This page specifies the boolean expression syntax implemented by ``esp_bool_parser`` for ESP-IDF-style manifest conditions. It is derived from the ESP-IDF ``idf-build-apps`` manifest reference and from the parser implementation and tests in this repository.

The purpose of this page is to document the effective parser contract. When the implementation behavior differs from higher-level ESP-IDF manifest prose, this reference follows the implementation.

*********
 Grammar
*********

At the top level, an expression consists of an atomic binary comparison or membership test, optionally combined with boolean operators.

.. code-block:: text

    [operand] [operator] [operand]

The parser does not accept a bare operand as a complete expression. For example, ``SOC_WIFI_SUPPORTED`` alone is invalid, whereas ``SOC_WIFI_SUPPORTED == 1`` is valid.

Boolean composition is supported through the infix operators ``and`` and ``or``.

Examples:

- ``IDF_TARGET == "esp32"``
- ``SOC_WIFI_SUPPORTED == 1``
- ``IDF_TARGET in ["esp32", "esp32s3"]``

**********
 Operands
**********

Uppercase identifiers
=====================

An identifier must start with an uppercase ASCII letter and may continue with uppercase ASCII letters, digits, and underscores. This matches names such as:

- ``IDF_TARGET``
- ``CONFIG_NAME``
- ``SOC_WIFI_SUPPORTED``
- ``ESP_ROM_HAS_SPI_FLASH``

Identifier resolution order
---------------------------

During evaluation, identifiers are resolved in the following order (from highest to lowest precedence):

1. attributes registered with :func:`esp_bool_parser.bool_parser.register_addition_attribute`
2. the built-in identifiers ``IDF_TARGET`` and ``CONFIG_NAME``
3. environment variables
4. other built-in identifiers, including ``IDF_VERSION``, ``IDF_VERSION_{MAJOR,MINOR,PATCH}`` and target-specific values loaded from SOC and ROM capability headers
5. the fallback value ``0``

Consequently, both an unknown identifier and an unset environment variable evaluate to ``0``.

Built-in identifiers
--------------------

The following identifiers have dedicated runtime handling in the parser:

.. list-table::
    :header-rows: 1

    - - Identifier
      - Runtime value
    - - ``IDF_TARGET``
      - The ``target`` argument passed to ``get_value()``
    - - ``CONFIG_NAME``
      - The ``config_name`` argument passed to ``get_value()``
    - - ``IDF_VERSION``
      - String in ``MAJOR.MINOR.PATCH`` form
    - - ``IDF_VERSION_MAJOR``
      - Integer ESP-IDF major version
    - - ``IDF_VERSION_MINOR``
      - Integer ESP-IDF minor version
    - - ``IDF_VERSION_PATCH``
      - Integer ESP-IDF patch version

String literals
===============

String literals must use double quotes.

Valid examples:

- ``"esp32"``
- ``"sdkconfig.ci"``
- ``"5.2.0"``

Invalid examples:

- ``'esp32'``
- ``esp32``

Integer literals
================

The grammar accepts:

- decimal non-negative integers such as ``0``, ``1``, and ``42``
- hexadecimal integers with a lowercase ``0x`` prefix such as ``0x0``, ``0x2A``, and ``0xAB``

Negative integers are not part of the grammar.

List literals
=============

List literals use square brackets and comma-separated literal elements.

Supported element types:

- strings
- integers
- mixed strings and integers

Examples:

- ``["esp32", "esp32s3"]``
- ``[1, 2, 3]``
- ``["esp32", 1, 0x2A]``

List elements must be literals. Variables, nested lists, and arbitrary expressions are not accepted inside a list literal.

***********
 Operators
***********

Comparison operators
====================

The following binary comparison operators are supported:

- ``==``
- ``!=``
- ``>``
- ``>=``
- ``<``
- ``<=``

Membership operators
====================

The following membership operators are supported:

- ``in``
- ``not in``

These operators are intended for membership tests against a list literal on the right-hand side, for example:

- ``IDF_TARGET in ["esp32", "esp32s3"]``
- ``IDF_VERSION not in ["5.0.0", "5.1.0"]``

The parser does not enforce the right-hand-side list constraint at parse time, but manifest-compatible expressions should keep the right operand as a list literal.

Boolean operators
=================

The following boolean operators are supported:

- ``and``
- ``or``

Parentheses may be used to control grouping explicitly.

***************************
 Precedence and evaluation
***************************

Operator precedence
===================

The parser gives ``and`` higher precedence than ``or``. Therefore:

.. code-block:: text

    A == 1 and B == 2 or C == 3

is evaluated as:

.. code-block:: text

    (A == 1 and B == 2) or C == 3

Use parentheses whenever grouping must be explicit or when mixed boolean operators could be ambiguous to readers.

Version-aware comparison
========================

``IDF_VERSION`` participates in version-aware ordering for ``==``, ``!=``, ``>``, ``>=``, ``<``, and ``<=``.

If either operand is already a ``packaging.version.Version`` instance, both operands are coerced through ``packaging.version.Version`` before comparison.

Examples:

- ``IDF_VERSION > "5.10.0"``
- ``IDF_VERSION <= "5.3.0"``

For ``in`` and ``not in``, version values are compared as strings rather than as ordered ``Version`` objects. For example:

- ``IDF_VERSION in ["5.9.0"]``

If version coercion fails during a version-aware comparison, evaluation raises ``InvalidInput``.

***************
 Invalid forms
***************

The following forms are either outside the accepted grammar or technically parseable but not suitable as manifest-compatible input:

.. list-table::
    :header-rows: 1

    - - Form
      - Status
      - Notes
    - - ``SOC_WIFI_SUPPORTED``
      - Invalid
      - A binary operator is required
    - - ``IDF_TARGET == 'esp32'``
      - Invalid
      - Strings must use double quotes
    - - ``FOO in BAR``
      - Discouraged
      - Parses, but the right operand should be a list
    - - ``["esp32"] == IDF_TARGET``
      - Valid but unusual
      - The grammar allows it, but it is not idiomatic input
    - - ``-1 == -1``
      - Invalid
      - Negative integers are not supported
    - - ``0X10 == 16``
      - Invalid
      - Hex literals require a lowercase ``0x`` prefix
    - - ``IDF_TARGET in [CONFIG_NAME]``
      - Invalid
      - List elements must be literals

****************
 Quick examples
****************

.. list-table::
    :header-rows: 1

    - - Expression
      - Effect
    - - ``IDF_TARGET == "esp32"``
      - target equality test
    - - ``CONFIG_NAME != "psram"``
      - config-name inequality test
    - - ``SOC_WIFI_SUPPORTED == 1``
      - capability flag comparison
    - - ``IDF_VERSION >= "5.3.0"``
      - version-aware ordering comparison
    - - ``IDF_TARGET in ["esp32", "esp32s3"]``
      - membership test over a literal list
