#!/usr/bin/env python3
"""
"""
__author__ = 'theodor.rodweil@victory-k.it'
__copyright__ = '2023 - Victory Karma IT'
__license__ = 'UNLICENSED'
__version__ = "1.0"

import sys
from pathlib import Path

# -- Project information -------------------------------------------------------

project = 'Default Sample'

copyright = __copyright__

author = __author__

# `release` is supported, yet some extensions still use the deprecated `version`
release = __version__
version = release

extensions = ['xconfluencebuilder']

exclude_patterns = ['Pipfile*', 'build', '.DS_Store', '.venv']

confluence_server_url = 'https://confluence.adesso.de/'

confluence_space_key = '~Tiara.Rodney@adesso.de'

confluence_publish = True

confluence_publish_dryrun = False

confluence_publish_token = 'OTI5NjA5ODc4MzQ5Oh1iD55oEGu7XKRazXHAW5p8mR5r'
