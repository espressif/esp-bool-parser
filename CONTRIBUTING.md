# Contributions Guide

Hi! We're glad that you're interested in contributing to `esp-bool-parser`. This document would guide you through the process of setting up the development environment, running tests, and building documentation.

## Supported ESP-IDF Versions

Here's a table shows the supported ESP-IDF versions and the corresponding Python versions.

| ESP-IDF Version | ESP-IDF Supported Python Versions | esp-bool-parser Releases |
|-----------------|-----------------------------------|--------------------------|
| 5.0             | 3.7+                              | main (0.x)               |
| 5.1             | 3.7+                              | main (0.x)               |
| 5.2             | 3.7+                              | main (0.x)               |
| 5.3             | 3.8+                              | main (0.x)               |
| 5.4             | 3.8+                              | main (0.x)               |
| master (5.5)    | 3.9+                              | main (0.x)               |

## Setup the Dev Environment

1. Create virtual environment

    ```shell
    python -m venv venv
    ```

2. Activate the virtual environment

    ```shell
    . ./venv/bin/activate
    ```

3. Install [flit][flit]

    We use [flit][flit] to build the package and install the dependencies.

    ```shell
    pip install flit
    ```

4. Install all dependencies

    All dependencies would be installed, and our package `esp-bool-parser` would be installed with editable mode.

    ```shell
    flit install -s
    ```

## Run Testing

We use [pytest][pytest] for testing.

```shell
pytest
```

## Build Documentation

We use [sphinx][sphinx] and [autodoc][autodoc] for generating documentation and API references. Besides, we treat warnings as errors while building the documentation. Please fix them before your commits got merged.

```shell
cd docs/en && make html
```

For documentation preview, you may use any browser you prefer. The executable has to be searchable in `PATH`. For example we're using firefox here.

```shell
firefox _build/html/index.html
```

[flit]: https://flit.pypa.io/en/stable/index.html
[pytest]: https://docs.pytest.org/en/stable/contents.html
[sphinx]: https://www.sphinx-doc.org/en/master/
[autodoc]: https://www.sphinx-doc.org/en/master/usage/quickstart.html#autodoc