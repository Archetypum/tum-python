# tum-python

![TheUnixManager](https://github.com/user-attachments/assets/6c0b3fbc-1d09-4d35-9dde-33b22a468c45)

--- 

## Overview

Tum (TheUnixManager) is a universal package management and system initialization library created by Archetypum, designed to simplify interactions with UNIX-like systems and streamline the development of system-related python scripts.

This is the Python implementation of `tum`.

---

## Table of contents

- [Why?](#why)
- [What does it solve?](#what-does-it-solve)
- [Use Cases](#use-cases)
- [Installation](#installation)
- [Documentation](#documentation)
- [Tests](#tests)
- [Supported Package Management Utilities (35)](#supported-package-management-utilities-35)
- [Supported Initialization Systems (7)](#supported-initialization-systems-7)
- [Example Usage](#example-usage)
- [Other Implementations by Archetypum](#other-implementations-by-archetypum)
- [Legal](#legal)

---

## Why?

Because interacting with countless package managers and init systems across UNIX-like platforms is painful — `tum` fixes that.

With `tum`, you:

1) Don't need to be a UNIX maniac who knows every package manager and init system syntax by heart;

2) Don't waste time building utilities from scratch — core functions are prebuilt and ready;

3) Don't write bloated, error-prone scripts — your code stays clean, readable, and portable.

## What does it solve?

Managing packages and system services is inconsistent across distros. Whether you're scripting for Arch, Debian, Void, Slackware, Red Hat, or others, `tum` provides a unified interface to abstract those differences.

It gives you:

1) A standardized way to install, remove, purge, update, upgrade packages (any many more!);

2) Unified service control (status, start, stop, enable, etc.) across multiple init systems (and many more);

3) A modular approach to extend support for more tools and distros;

4) Shell-friendly integration for faster development and cleaner scripts.


## Use Cases

- Write portable installation scripts that “just work” on most UNIX-like systems;

- Build lightweight system provisioning tools in pure python;

- Create consistent automation for servers, containers, or virtual machines;

- Prototype cross-distro sysadmin tools without rewriting core logic.

---

## Installation

- Via `pip`:

```sh
pip install the_unix_manager
```

- Manual Bulinding:

```sh
git clone https://github.com/Archetypum/tum-python.git
cd tum-python/

pip install -r requirements.txt
python3 setup.py
```

## Documentation

All `tum-python` functions, classes and methods have a lot of documentation. You can check it inside your code editor.

## Tests

You can find automatic tests inside the `t/` directory.

If you want test your installation manually:

```sh
python3 autotests.py
```

## Supported Package Management Utilities (35)

### Debian-based:

- **apt**, **apt-get**, **apt-cache**, **apt-cdrom**, **apt-config**, **apt-extracttemplates**, **apt-listchanges**, **apt-mark**, **apt-sortpkgs**, **aptitude**, **aptitude-create-state-bundle**, **aptitude-run-state-bundle**, **dpkg**

### Arch-based:

- **pacman**, **yay**, **trizen**, **pamac**

### Gentoo-based:

- **portage** (open for pull requests)

### Slackware-based:

- **slackpkg**

### Alpine-based:

- **apk**

### Void-based:

- **xbps-install**, **xbps-remove**, **xbps-query**

### Guix-based:

- **guix**

### Dragora-based:

- **qi**

### OpenBSD/NetBSD/FreeBSD-based:

- **pkg_add**, **pkg_delete**, **pkg_create**, **pkg_info**

### FreeBSD-based:

- **pkg**

### NetBSD-based:

- **pkgin**

### RedHat-based:

- **yum**, **dnf**

### openSUSE-based:

- **zypper**, **zypper-log**

### macOS-based:

- **homebrew**

## Supported Initialization Systems (7)

- **systemd**

- **sysvinit**

- **openrc**

- **runit**

- **s6**

- **dinit**

- **launchd**

## Example Usage

### UNIX:

```python

```

### Service Management:

```python

```

### Package Management

```python

```

## Other Implementations by Archetypum

- [_tum-bash_](https://github.com/Archetypum/tum-bash)

- [_tum-perl_](https://github.com/Archetypum/tum-perl)

- [_tum-raku_](https://github.com/Archetypum/tum-raku)

- [_tum-lua_](https://github.com/Archetypum/tum-lua)

- [_tum-c_](https://github.com/Archetypum/tum-c)

- [_tum-rust_](https://github.com/Archetypum/tum-rust)

## Legal

**tum-python** is free software, released under the **GNU Lesser General Public License v3**.

See:

- [_LICENSE-LGPLv3.md_](https://github.com/Archetypum/tum-python/blob/master/LICENSE-LGPLv3.md)

- _https://www.gnu.org/licenses/lgpl-3.0.html_

- [_Free Software Foundation_](https://www.fsf.org/)

![GNU](https://github.com/user-attachments/assets/66935a97-374f-4dbc-9f1c-428070fda139)
