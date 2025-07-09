esp-bool-parser |version| Documentation
=======================================

This documentation is for esp-bool-parser. esp-bool-parser is a package which help process boolean statements based on ``soc_caps`` files in the ESP-IDF.

esp-bool-parser
---------------

``esp-bool-parser`` is a package that provides a way to process boolean statements based on ``soc_caps`` files in the ESP-IDF.

It helps you locate ``soc_headers`` files in the ESP-IDF, parse them, and store the parsed values as constants, which are then used in ``ChipAttr``.

When you import ``esp_bool_parser``, you will gain access to ``parse_bool_expr``.

Usage Example
-------------

.. code-block:: python

    stmt_string = 'IDF_TARGET == "esp32"'
    stmt: BoolStmt = parse_bool_expr(stmt_string)
    result = stmt.get_value("esp32", "config_name")

Extendability
-------------

You can extend the functionality of ``ChipAttr`` by adding custom handlers for new attributes. Use the ``register_addition_attribute`` function to register additional attributes. When these attributes are encountered, the associated handler function will be called. Additionally, you can override existing attributes, as the newly registered handler will take priority over the original ones.

Example:

.. code-block:: python

    def custom_handler(target: str, config_name: str, **kwargs) -> Any:
        # Custom logic to handle the attribute
        return "custom_value"


    register_addition_attribute("CUSTOM_ATTR", custom_handler)

.. caution::

    Always add ``**kwargs`` to keep forward-compatibility.

.. toctree::
    :maxdepth: 1
    :caption: API Reference

    api/modules

.. toctree::
    :maxdepth: 1
    :caption: Others
    :glob:

    others/*
