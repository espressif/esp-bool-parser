###############
 API Reference
###############

Complete API documentation for the ``esp-bool-parser`` package.

************
 Components
************

**Boolean Expression Parser**
    Parse and evaluate boolean expressions for ESP-IDF targets and configurations

**SOC Header Parser**
    Extract chip capabilities from ESP-IDF SOC header files

**Extensible Attributes**
    Register custom attributes and handlers for specialized use cases

**Constants and Utilities**
    ESP-IDF constants and utility functions

****************
 Core Functions
****************

``parse_bool_expr()``
    Parse boolean expressions and return BoolStmt objects

``register_addition_attribute()``
    Register custom attributes for ChipAttr

``BoolStmt.get_value()``
    Evaluate boolean expressions for specific targets

***********************
 Package Documentation
***********************

.. toctree::
    :maxdepth: 2

    esp_bool_parser
