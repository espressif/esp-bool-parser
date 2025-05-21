# Changelog

All notable changes to this project will be documented in this file.

## v0.1.3 (2025-05-21)

### Perf

- add lru_cache for all `get_value`
- use `any` or `all` instead of for-loop

## v0.1.2 (2025-01-07)

### Feat

- module level lazy load

### Fix

- add BoolStrm to __all__

## v0.1.1 (2025-01-07)

### Feat

- add py.typed file

## v0.1.0 (2025-01-02)

### Added

- **`parse_bool_expr`**: A method for handling complex boolean expressions, supporting logical operators like `and` and `or`.
- **`register_addition_attribute`**: A method for dynamically registering additional attributes with the `ChipAttr` class, enabling custom attribute handling for targets and configurations.
