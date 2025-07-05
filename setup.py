#!/usr/bin/env python3

"""
:authors: Archetypum
:license: GNU Lesser General Public License v3, see LICENSE-LGPLv3.md
:copyright: (c) 2025 Archetypum
"""

import sys

try:
    from setuptools import setup, find_packages
except ModuleNotFoundError as import_error:
    print(f"[!] Error: {import_error}")
    sys.exit(1)

tum_name: str = "tum"
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

