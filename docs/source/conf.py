import os
import sys

# Añadir una descripción general de lo que hace este bloque de código.
sys.path.insert(0, os.path.abspath('/home/ara/IS2_2023/proyecto_CMS'))
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

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Ajustes adicionales para mejorar la apariencia:
html_theme_options = {
    'collapse_navigation': False,  # Mantiene la navegación expandida.
    'sticky_navigation': True,  # Hace que la navegación se quede "pegada" en la parte superior.
    'navigation_depth': 4,  # Profundidad de la navegación.
    'includehidden': True,  # Incluye títulos ocultos en la navegación.
    'titles_only': False  # Solo muestra títulos en la navegación, no subsecciones.
}
# Si deseas personalizar los colores, estilos, etc., puedes hacerlo mediante archivos CSS personalizados y añadirlos a la lista:
html_css_files = [
    'custom.css',  # Asegúrate de crear este archivo en tu directorio '_static' y añadir tus estilos personalizados allí.
]