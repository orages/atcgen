# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'atcgen'
copyright = '2021, Epitanime'
author = 'Epitanime Toyunda Dev Team'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "rst2pdf.pdfbuilder"
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# generate builtin_instructions.rst file
from os.path import join as pjoin, dirname
import importlib
import sys
atcgen_path = dirname(dirname(__file__))
finder = importlib.machinery.FileFinder(atcgen_path)
spec = finder.find_spec(
    "atcgen",
    pjoin(atcgen_path, "atcgen"))
atcgen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(atcgen)
if "atcgen" not in sys.modules:
    sys.modules["atcgen"] = atcgen
importlib.import_module("atcgen.generator")
instructions_help = atcgen.generator.Generator().get_instructions_help()
doc_directory = dirname(__file__)
with open(pjoin(doc_directory,
                "general", "builtin_instructions.rst"), mode="w+",
          encoding="utf-8") as f:
    f.write("..\n\tGenerated at sphinx build. DO NOT EDIT.\n\n\n")
    f.write("************\nInstructions\n************\n\n")
    f.write(instructions_help)
