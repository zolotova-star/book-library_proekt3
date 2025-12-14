# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Путь к проекту ---------------------------------------------------------
# Критически важно для импорта модулей!
sys.path.insert(0, os.path.abspath('../../'))

# -- Project information -----------------------------------------------------
project = 'Book Library'
copyright = '2025, Dasha'
author = 'Dasha'
release = '1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',      # Для автоматической документации из docstrings
    'sphinx.ext.napoleon',     # Для поддержки Google/NumPy стилей
    'sphinx.ext.viewcode',     # Показывать исходный код
]

# Настройки для napoleon (чтобы работали Google-style докстринги)
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True

templates_path = ['_templates']
exclude_patterns = []

# Язык документации
language = 'ru'

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'  # Важно: именно эта тема!

# Настройки для темы RTD
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
}

html_static_path = ['_static']
html_show_sourcelink = True

# Чтобы модули не показывались с префиксом 'booklib.'
add_module_names = False