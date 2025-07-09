#!/usr/bin/env python3
#
# `tum/trizen.py`
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


def trizen(*args: str) -> None:
    safe_execute(["trizen", *args])


def trizen_sync(*args: str) -> None:
    safe_execute(["trizen", "--sync", *args])


def trizen_comments(*args: str) -> None:
    safe_execute(["trizen", "--comments", *args])


def trizen_get(*args: str) -> None:
    safe_execute(["trizen", "--get", *args])


def trizen_remove(*args: str) -> None:
    safe_execute(["trizen", "--remove", *args])


def trizen_query(*args: str) -> None:
    safe_execute(["trizen", "--query", *args])


def trizen_files(*args: str) -> None:
    safe_execute(["trizen", "--files", *args])


def trizen_database(*args: str) -> None:
    safe_execute(["trizen", "--database", *args])


def trizen_deptest(*args: str) -> None:
    safe_execute(["trizen", "--deptest", *args])


def trizen_upgrade(*args: str) -> None:
    safe_execute(["trizen", "--upgrade", *args])
