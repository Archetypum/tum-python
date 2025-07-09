#!/usr/bin/env python3
#
# `tum/pamac.py`
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

try:
    import re
    import sys
    import typing
    import subprocess

    RED: str = "\033[0;31m"
    GREEN: str = "\033[0;32m"
    RESET: str = "\033[0m"

    SAFE_ARG_PATTERN: re.Pattern[str] = re.compile(r"^[\w@.+:/=-]+$")
except ModuleNotFoundError as import_error:
    print(f"[!] Error:\n{import_error}")
    sys.exit(1)


class TumExecutionError(Exception):
    pass


class UnsafeInputError(TumExecutionError):
    arg: str

    def __init__(self, arg: str) -> None:
        self.arg = arg
        super().__init__(f"Unsafe or invalid argument detected: '{arg}'")


class CommandNotFoundError(TumExecutionError):
    binary: str

    def __init__(self, binary: str) -> None:
        self.binary = binary
        super().__init__(f"Command not found: '{binary}'")


class ExecutionFailedError(TumExecutionError):
    cmd: typing.List[str]
    returncode: int
    stdout: str
    stderr: str

    def __init__(self, cmd: typing.List[str], returncode: int, stdout: str, stderr: str) -> None:
        self.cmd = cmd
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        message: str = f"Execution failed: {' '.join(cmd)}\nExit code: {returncode}\n{stderr.strip()}"
        super().__init__(message)


def is_safe_argument(arg: str) -> bool:
    return bool(SAFE_ARG_PATTERN.fullmatch(arg))


def validate_command(cmd: typing.List[str]) -> None:
    if not cmd:
        raise UnsafeInputError("Empty command list")

    for arg in cmd:
        if not arg or not is_safe_argument(arg):
            raise UnsafeInputError(arg)


def safe_execute(cmd: typing.List[str]) -> None:
    print(f"{GREEN}[<==] Executing '{' '.join(cmd)}'...{RESET}")
    validate_command(cmd)

    try:
        result: subprocess.CompletedProcess[str] = subprocess.run(cmd, check=True, capture_output=True, text=True)

        if result.stdout:
            print(result.stdout)

        print(f"{GREEN}[*] Success!{RESET}")

    except FileNotFoundError:
        raise CommandNotFoundError(cmd[0])

    except subprocess.CalledProcessError as execution_error:
        raise ExecutionFailedError(cmd, execution_error.returncode, execution_error.stdout, execution_error.stderr)


def pamac(*args: str) -> None:
    return safe_execute(["pamac", *args])


def pamac_version(*args: str) -> None:
    return safe_execute(["pamac", "--version", *args])


def pamac_help(*args: str) -> None:
    return safe_execute(["pamac", "--help", *args])


def pamac_search(*args: str) -> None:
    return safe_execute(["pamac", "search", *args])


def pamac_list(*args: str) -> None:
    return safe_execute(["pamac", "list", *args])


def pamac_info(*args: str) -> None:
    return safe_execute(["pamac", "info", *args])


def pamac_install(*args: str) -> None:
    return safe_execute(["pamac", "install", *args])


def pamac_reinstall(*args: str) -> None:
    return safe_execute(["pamac", "reinstall", *args])


def pamac_remove(*args: str) -> None:
    return safe_execute(["pamac", "remove", *args])


def pamac_checkupdates(*args: str) -> None:
    return safe_execute(["pamac", "checkupdates", *args])


def pamac_upgrade(*args: str) -> None:
    return safe_execute(["pamac", "upgrade", *args])


def pamac_update(*args: str) -> None:
    return safe_execute(["pamac", "update", *args])


def pamac_clone(*args: str) -> None:
    return safe_execute(["pamac", "clone", *args])


def pamac_build(*args: str) -> None:
    return safe_execute(["pamac", "build", *args])


def pamac_clean(*args: str) -> None:
    return safe_execute(["pamac", "clean", *args])
