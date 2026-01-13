#########################################
 esp-bool-parser |version| Documentation
#########################################

esp-bool-parser processes boolean expressions based on ESP-IDF ``soc_caps`` files.

**********
 Overview
**********

This package parses boolean statements from ESP-IDF configurations and evaluates them against target-specific capabilities. It locates SOC header files, extracts chip capabilities, and stores them as constants for use in ``ChipAttr``.

The main entry point is ``parse_bool_expr``, which returns a ``BoolStmt`` object for evaluation.

*******
 Usage
*******

.. code-block:: python

    from esp_bool_parser import parse_bool_expr

    stmt = parse_bool_expr('IDF_TARGET == "esp32"')
    result = stmt.get_value("esp32", "config_name")

********************
 Extending ChipAttr
********************

Register custom attributes using ``register_addition_attribute``. Custom handlers take priority over built-in attributes.

.. code-block:: python

    def custom_handler(target: str, config_name: str, **kwargs) -> Any:
        return "custom_value"


    register_addition_attribute("CUSTOM_ATTR", custom_handler)

.. caution::

    Always include ``**kwargs`` for forward compatibility.

.. toctree::
    :maxdepth: 2
    :caption: API Reference

    api/modules

.. toctree::
    :maxdepth: 1
    :caption: Others
    :glob:

    others/*
