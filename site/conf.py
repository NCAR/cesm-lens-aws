# -- Project information -----------------------------------------------------
import datetime

project = 'CESM1 LENS data on AWS S3'
copyright = f'{datetime.datetime.now().year}, National Center for Atmospheric Research'
author = 'Science @ Scale Team'
html_last_updated_fmt = '%b %d, %Y'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'myst_nb',
    'sphinx_panels',
    'sphinx_copybutton',
    'sphinx_comments',
]

comments_config = {
    'utterances': {'repo': 'NCAR/cesm-lens-aws', 'optional': 'config', 'label': '💬 comment'},
    'hypothesis': False,
}

jupyter_execute_notebooks = 'off'
# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '.github']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_book_theme'

html_title = project

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_logo = '_static/logo.png'
html_favicon = '_static/favicon.ico'

show_navbar_depth = 3
html_theme_options = {
    'repository_url': 'https://github.com/NCAR/cesm-lens-aws',
    'repository_branch': 'main',
    'use_repository_button': True,
    'use_edit_page_button': True,
    'extra_navbar': '',
}
myst_enable_extensions = [
    'colon_fence',
    'deflist',
    'linkify',
]
myst_url_schemes = ['https', 'http', 'ftp', 'mailto']
intersphinx_mapping = {}

panels_add_bootstrap_css = False
