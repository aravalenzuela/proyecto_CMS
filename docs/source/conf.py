import os
import sys
sys.path.insert(0, os.path.abspath('/home/ubuntu/Escritorio/IS2_STAGING/proyecto_CMS'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'  # Reemplaza 'core.settings' con la ubicación real de tu archivo settings si es diferente.
import django
django.setup()

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Sistema de gestión de contenidos'
copyright = '2023, EQUIPO_04_FPUNA'
author = 'EQUIPO_04_FPUNA'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc'
]

templates_path = ['_templates']
exclude_patterns = []

language = 'es'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
