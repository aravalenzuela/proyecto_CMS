import sys
import os

sys.path.insert(0, os.path.abspath('/home/ubuntu/Escritorio/IS2_STAGING/proyecto_CMS'))
                
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'proyecto_CMS'
copyright = '2023, IS2-GRUPO-4'
author = 'IS2-GRUPO-4'
release = 'version 1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    # ... otras extensiones
]

templates_path = ['_templates']
exclude_patterns = []

language = 'Python, HTML, Docker, CSS'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
