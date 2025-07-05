#!/usr/bin/python3
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
# You should have received a copy of the GNU General Public License
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
    from .dinit import *
    from .launchd import *
    from .openrc import *
    from .runit import *
    from .s6 import *
    from .systemd import *
    from .sysvinit import *

    # Package Managers:
    from .apk import *
    from .apt import *
    from .apt_cache import *
    from .apt_cdrom import *
    from .apt_config import *
    from .apt_extracttemplates import *
    from .apt_get import *
    from .apt_listchanges import *
    from .apt_mark import *
    from .apt_sortpkgs import *
    from .aptitude import *
    from .aptitude_create_state_bundle import *
    from .dng import *
    from .dpkg import *
    from .guix import *
    from .homebrew import *
    from .pacman import *
    from .pamac import *
    from .pkg import *
    from .pkg_add import *
    from .pkg_create import *
    from .pkg_delete import *
    from .pkg_info import *
    from .pkgin import *
    from .portage import *
    from .qi import *
    from .slackpkg import *
    from .trizen import *
    from .xbps_install import *
    from .xbps_query import *
    from .xbps_remove import *
    from .yay import *
    from .yum import *
    from .zypper import *
    from .zypper_log import *
except ModuleNotFoundError as import_error:
    print(f"[!] Error: {import_error}")

__author__: str = "Archetypum"
__version__: str = "0.0.1"
__email__: str = "archetypum@tutamail.com"

