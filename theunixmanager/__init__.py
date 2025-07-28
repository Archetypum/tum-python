#!/usr/bin/env python3
#
# `theunixmanager/__init__.py`
#
# Copyright (C) 2025 Archetypum
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>

"""
:authors: Archetypum
:license: GNU Lesser General Public License v3, see LICENSE-LGPLv3.md file.

:copyright: (c) 2025 Archetypum 
"""

try:
    # UNIX:
    from .unix import *

    # Init systems:
    from .initmanagement import *

    # Package Managers:
    from .packagemanagement import *
except ModuleNotFoundError as import_error:
    print(f"[!] Error: {import_error}")

__author__: str = "Archetypum"
__version__: str = "0.0.1"
__email__: str = "archetypum@tutamail.com"

