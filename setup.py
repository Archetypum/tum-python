#!/usr/bin/env python3
#
# `setup.py`
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
:license: GNU Lesser General Public License v3, see LICENSE-LGPLv3.md
:copyright: (c) 2025 Archetypum
"""

try:
    import sys
    from setuptools import setup, find_packages
except ModuleNotFoundError as import_error:
    print(f"[!] Error: {import_error}")
    sys.exit(1)

tum_name: str = "theunixmanager"
tum_version: str = "0.0.1"
tum_license: str = "LGPL-3.0-or-later"
tum_author: str = "Archetypum"
tum_author_email: str = "archetypum@tutamail.com"
tum_short_description: str = "Easy cross-platform UNIX scripting with Python."
tum_long_description: str = ""
tum_github_url: str = "https://github.com/Archetypum/tum-python"
tum_releases_url: str = "https://github.com/Archetypum/tum-python/releases"

setup(
    name=tum_name,
    version=tum_version,
    license=tum_license,
    author=tum_author,
    author_email=tum_author_email,
    description=tum_short_description,
    long_description=tum_long_description,
    long_description_content_type="text/markdown",
    url=tum_github_url,
    download_url=tum_releases_url,
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.10",
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: Unix",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries",
    ],
)
