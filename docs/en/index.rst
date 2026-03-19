#########################################
 esp-bool-parser |version| Documentation
#########################################

``esp-bool-parser`` parses and evaluates ESP-IDF-style boolean expressions against target metadata derived from ESP-IDF ``soc_caps`` headers and runtime context.

**********
 Overview
**********

The package is intended for tools that need to evaluate manifest-style conditions such as target checks, configuration-name checks, version predicates, and capability-gated expressions.

When SOC/ROM capability information is first needed (for example, during a capability lookup), the library discovers relevant ESP-IDF SOC capability headers, extracts capability macros, and exposes them to the expression evaluator through identifier resolution.

The primary entry point is ``parse_bool_expr()``, which parses an expression and returns a ``BoolStmt`` instance. The resulting object can then be evaluated with ``BoolStmt.get_value()`` for a specific ``target`` and ``config_name``.

*******
 Usage
*******

.. code-block:: python

    from esp_bool_parser import parse_bool_expr

    stmt = parse_bool_expr('IDF_TARGET == "esp32"')
    result = stmt.get_value("esp32", "config_name")

In this example, the parser produces an executable expression object and evaluates it in the context of the ``esp32`` target and the provided configuration name.

********************
 Extending ChipAttr
********************

Register custom identifier resolvers with ``register_addition_attribute()`` when the default evaluation context is not sufficient.

Custom handlers are consulted before built-in identifier handling, environment variables, and SOC-derived capability values. This allows integrations to inject tool-specific state or override the value of an existing identifier deliberately.

.. code-block:: python

    def custom_handler(target: str, config_name: str, **kwargs) -> Any:
        return "custom_value"


    register_addition_attribute("CUSTOM_ATTR", custom_handler)

.. caution::

    Always include ``**kwargs`` for forward compatibility.

.. toctree::
    :maxdepth: 1
    :caption: References
    :glob:

    references/*

.. toctree::
    :maxdepth: 1
    :caption: Others
    :glob:

    others/*
