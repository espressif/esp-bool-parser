# SPDX-FileCopyrightText: 2023-2025 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0


# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
from datetime import datetime

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'esp-bool-parser'
project_homepage = 'https://github.com/espressif/esp-bool-parser'
copyright = f'2024-{datetime.now().year}, Espressif Systems (Shanghai) Co., Ltd.'  # noqa: A001
author = 'Fu Hanxi'
languages = ['en']
version = '0.x'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx_copybutton',
    'myst_parser',
    'sphinxcontrib.mermaid',
    'sphinxarg.ext',
    'sphinx_tabs.tabs',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_css_files = ['theme_overrides.css']
html_logo = '../_static/espressif-logo.svg'
html_static_path = ['../_static']
html_theme = 'sphinx_rtd_theme'


autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'member-order': 'bysource',
    'show-inheritance': True,
    'exclude-members': 'model_computed_fields,model_config,model_fields,model_post_init',
}
