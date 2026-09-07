# esp-bool-parser

`esp-bool-parser` is a package that provides a way to process boolean statements based on `soc_caps` files in the ESP-IDF.

It helps you locate `soc_headers` files in the ESP-IDF, parse them, and store the parsed values as constants, which are then used in `ChipAttr`.

When you import `esp_bool_parser`, you will gain access to the following functions:

### Key Functions

#### `parse_bool_expr(stmt: str)`

Parses a boolean expression.

- **Parameters:**
    - `stmt` (str): A string containing the boolean expression.

- **Returns:**
    - A parsed representation of the boolean expression.

- **Usage Example:**

  ```python
  stmt_string = 'IDF_TARGET == "esp32"'
  stmt = parse_bool_expr(stmt_string)
  result = stmt.get_value('esp32', 'config_name')
  ```

#### `register_addition_attribute(attr: str, action: t.Callable[..., t.Any]) -> None`

Registers an additional attribute for `ChipAttr`.

You can extend the functionality of `ChipAttr` by adding custom handlers for new attributes.
Use the `register_addition_attribute` function to register additional attributes.
When these attributes are encountered, the associated handler function will be called.
Additionally, you can override existing attributes, as the newly registered handler will take priority over the original ones.

- **Parameters:**
  - `attr` (str): The name of the additional attribute.
  - `action` (Callable): A callable that processes `**kwargs`. The `target` and `config_name` parameters will be passed as `kwargs` when the attribute is detected.

- **Usage Example:**

  ```python
  def my_action(target, config_name, **kwargs):
      # Custom logic to handle the attribute
      print(f'Processing {target} with {config_name}')
      return target


  register_addition_attribute('CUSTOM_ATTR', my_action)
  ```
