# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "file_tree_check"
copyright = "2023, Bertrand Toutée"
author = "Bertrand Toutée"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    "sphinx_copybutton",
    "myst_parser",
    "sphinxarg.ext",
]
matlab_src_dir = os.path.dirname(os.path.abspath("../../src"))

templates_path = ["_templates"]
exclude_patterns = []

suppress_warnings = ["myst.header"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# The master toctree document.
master_doc = "index"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_theme_options = {
    "collapse_navigation": False,
    "display_version": False,
    "navigation_depth": 4,
}
myst_heading_anchors = 2
