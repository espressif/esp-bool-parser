API Reference
=============

This section provides detailed API reference documentation for the ``esp-bool-parser`` package.

Overview
--------

The ``esp-bool-parser`` package provides the following main components:

- **Boolean Expression Parser**: Parse and evaluate boolean expressions with support for ESP-IDF targets and configurations
- **SOC Header Parser**: Parse ESP-IDF SOC header files to extract chip capabilities
- **Extensible Attributes**: Add custom attributes and handlers for specialized use cases
- **Constants and Utilities**: Access ESP-IDF constants and utility functions

Main Entry Points
-----------------

The primary functions you'll use are:

- ``parse_bool_expr()``: Parse boolean expressions and create BoolStmt objects
- ``register_addition_attribute()``: Register custom attributes for ChipAttr
- ``BoolStmt.get_value()``: Evaluate boolean expressions for specific targets

Package Documentation
---------------------

.. toctree::
    :maxdepth: 2

    esp_bool_parser
