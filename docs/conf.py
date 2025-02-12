#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# OCDS documentation build configuration file, created by
# sphinx-quickstart on Fri Dec 11 15:07:47 2015.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.


# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['myst_parser', 'sphinxcontrib.jsonschema', 'sphinxcontrib.opendataservices']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffixes of source filenames.
source_suffix = ['.rst', '.md']

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'sphinxcontrib-opendataservices'
copyright = '2017 Open Data Services, released under the MIT license'
author = 'Open Data Services'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output ----------------------------------------------

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Output file base name for HTML help builder.
htmlhelp_basename = 'OCDSdoc'

# The theme to use for HTML and HTML Help pages.
html_theme = "odsc_default_sphinx_theme"

locale_dirs = ['locale/']   # path is example but recommended.
gettext_compact = False     # optional.
