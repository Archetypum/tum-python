#!/usr/bin/env python3
#
# `theunixmanager/packagemanagement.py`
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
    """
    Base exception for errors raised by the Tum execution system.
    
    All execution-related exceptions should inherit from this class.
    """

    pass


class UnsafeInputError(TumExecutionError):
    """
    Raised when an unsafe or invalid argument is detected in the input.

    Attributes:
        arg (str): The argument that failed validation.
    """

    arg: str

    def __init__(self, arg: str) -> None:
        """
        Initialize an UnsafeInputError.

        Args:
            arg (str): The unsafe or invalid argument.
        """

        self.arg = arg
        super().__init__(f"Unsafe or invalid argument detected: '{arg}'")


class CommandNotFoundError(TumExecutionError):
    """
    Raised when a specified command is not found in the system.

    Attributes:
        binary (str): The name of the missing executable.
    """

    binary: str

    def __init__(self, binary: str) -> None:
        """
        Initialize a CommandNotFoundError.

        Args:
            binary (str): The command/executable that could not be found.
        """

        self.binary = binary
        super().__init__(f"Command not found: '{binary}'")


class ExecutionFailedError(TumExecutionError):
    """
    Raised when a subprocess command executes but fails (non-zero exit code).

    Attributes:
        cmd (List[str]): The command that was executed.
        returncode (int): The exit code returned by the subprocess.
        stdout (str): The standard output from the command.
        stderr (str): The standard error from the command.
    """

    cmd: typing.List[str]
    returncode: int
    stdout: str
    stderr: str
    message: str

    def __init__(self, cmd: typing.List[str], returncode: int, stdout: str, stderr: str) -> None:
        """
        Initialize an ExecutionFailedError.

        Args:
            cmd (List[str]): The command that failed.
            returncode (int): The exit code of the process.
            stdout (str): Captured standard output.
            stderr (str): Captured standard error.
        """

        self.cmd = cmd
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        message = f"Execution failed: {' '.join(cmd)}\nExit code: {returncode}\n{stderr.strip()}"
        super().__init__(message)


def is_safe_argument(arg: str) -> bool:
    """
    Validate if a given command-line argument is safe to use.

    This uses a pre-defined regular expression pattern (SAFE_ARG_PATTERN)
    to ensure the argument does not contain unsafe characters.

    Args:
        arg (str): The argument to validate.

    Returns:
        bool: True if the argument is safe, False otherwise.

    Example:
        >>> is_safe_argument("ls")
        True

        >>> is_safe_argument("rm -rf /")
        False
    """

    return bool(SAFE_ARG_PATTERN.fullmatch(arg))


def validate_command(cmd: typing.List[str]) -> None:
    """
    Validate a list of command-line arguments before execution.

    Ensures:
    - The list is not empty
    - Each argument matches the safety pattern

    Args:
        cmd (List[str]): The command to validate.

    Raises:
        UnsafeInputError: If any argument is missing or unsafe.

    Example:
        >>> validate_command(["ls", "-l"])
        # Passes

        >>> validate_command(["; rm -rf /"])
        # Raises UnsafeInputError
    """

    if not cmd:
        raise UnsafeInputError("Empty command list")

    for arg in cmd:
        if not arg or not is_safe_argument(arg):
            raise UnsafeInputError(arg)


def safe_execute(cmd: typing.List[str]) -> None:
    """
    Safely execute a command in a subprocess with validation and error handling.

    Steps:
    - Validates the command using `validate_command()`
    - Runs the command via `subprocess.run()`
    - Captures and prints stdout
    - Raises structured errors on failure

    Args:
        cmd (List[str]): The command to execute as a list of strings.

    Raises:
        UnsafeInputError: If the command contains invalid arguments.
        CommandNotFoundError: If the command binary is not found.
        ExecutionFailedError: If the command returns a non-zero exit code.

    Example:
        >>> safe_execute(["ls", "-l"])
        [<==] Executing 'ls -l'...
        total 0
        [*] Success!
    """
    
    print(f"{GREEN}[<==] Executing '{' '.join(cmd)}'...{RESET}")
    validate_command(cmd)

    try:
        result: subprocess.CompletedProcess[str] = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )

        if result.stdout:
            print(result.stdout)

        print(f"{GREEN}[*] Success!{RESET}")

    except FileNotFoundError:
        raise CommandNotFoundError(cmd[0])

    except subprocess.CalledProcessError as execution_error:
        raise ExecutionFailedError(
            cmd,
            execution_error.returncode,
            execution_error.stdout,
            execution_error.stderr
        )


#
# `apk`:
#
def apk(*args: str)                                       -> None: return safe_execute(["apk", *args])
def apk_help(*args: str)                                  -> None: return safe_execute(["apk", "--help", *args])
def apk_add(*args: str)                                   -> None: return safe_execute(["apk", "add", *args])
def apk_del(*args: str)                                   -> None: return safe_execute(["apk", "del", *args])
def apk_fix(*args: str)                                   -> None: return safe_execute(["apk", "fix", *args])
def apk_update(*args: str)                                -> None: return safe_execute(["apk", "update", *args])
def apk_upgrade(*args: str)                               -> None: return safe_execute(["apk", "upgrade", *args])
def apk_cache(*args: str)                                 -> None: return safe_execute(["apk", "cache", *args])
def apk_info(*args: str)                                  -> None: return safe_execute(["apk", "info", *args])
def apk_list(*args: str)                                  -> None: return safe_execute(["apk", "list", *args])
def apk_dot(*args: str)                                   -> None: return safe_execute(["apk", "dot", *args])
def apk_policy(*args: str)                                -> None: return safe_execute(["apk", "policy", *args])
def apk_search(*args: str)                                -> None: return safe_execute(["apk", "search", *args])
def apk_index(*args: str)                                 -> None: return safe_execute(["apk", "index", *args])
def apk_fetch(*args: str)                                 -> None: return safe_execute(["apk", "fetch", *args])
def apk_manifest(*args: str)                              -> None: return safe_execute(["apk", "manifest", *args])
def apk_verify(*args: str)                                -> None: return safe_execute(["apk", "verify", *args])
def apk_audit(*args: str)                                 -> None: return safe_execute(["apk", "audit", *args])
def apk_stats(*args: str)                                 -> None: return safe_execute(["apk", "stats", *args])
def apk_version(*args: str)                               -> None: return safe_execute(["apk", "version", *args])
#
# `apt`:
#
def apt(*args: str)                                       -> None: return safe_execute(["apt", *args])
def apt_autoclean(*args: str)                             -> None: return safe_execute(["apt", "autoclean", *args])
def apt_autoremove(*args: str)                            -> None: return safe_execute(["apt", "autoremove", *args])
def apt_changelog(*args: str)                             -> None: return safe_execute(["apt", "changelog", *args])
def apt_depends(*args: str)                               -> None: return safe_execute(["apt", "depends", *args])
def apt_download(*args: str)                              -> None: return safe_execute(["apt", "download", *args])
def apt_full_upgrade(*args: str)                          -> None: return safe_execute(["apt", "full-upgrade", *args])
def apt_install(*args: str)                               -> None: return safe_execute(["apt", "install", *args])
def apt_moo(*args: str)                                   -> None: return safe_execute(["apt", "moo", *args])
def apt_purge(*args: str)                                 -> None: return safe_execute(["apt", "purge", *args])
def apt_reinstall(*args: str)                             -> None: return safe_execute(["apt", "reinstall", *args])
def apt_search(*args: str)                                -> None: return safe_execute(["apt", "search", *args])
def apt_showsrc(*args: str)                               -> None: return safe_execute(["apt", "showsrc", *args])
def apt_update(*args: str)                                -> None: return safe_execute(["apt", "update", *args])
def apt_autopurge(*args: str)                             -> None: return safe_execute(["apt", "autopurge", *args])
def apt_build_dep(*args: str)                             -> None: return safe_execute(["apt", "build-dep", *args])
def apt_clean(*args: str)                                 -> None: return safe_execute(["apt", "clean", *args])
def apt_dist_upgrade(*args: str)                          -> None: return safe_execute(["apt", "dist-upgrade", *args])
def apt_edit_sources(*args: str)                          -> None: return safe_execute(["apt", "edit-sources", *args])
def apt_help(*args: str)                                  -> None: return safe_execute(["apt", "help", *args])
def apt_list(*args: str)                                  -> None: return safe_execute(["apt", "list", *args])
def apt_policy(*args: str)                                -> None: return safe_execute(["apt", "policy", *args])
def apt_rdepends(*args: str)                              -> None: return safe_execute(["apt", "rdepends", *args])
def apt_remove(*args: str)                                -> None: return safe_execute(["apt", "remove", *args])
def apt_show(*args: str)                                  -> None: return safe_execute(["apt", "show", *args])
def apt_source(*args: str)                                -> None: return safe_execute(["apt", "source", *args])
def apt_upgrade(*args: str)                               -> None: return safe_execute(["apt", "upgrade", *args])
#
# `apt-cache`:
#
def apt_cache(*args: str)                                 -> None: return safe_execute(["apt-cache", *args])
def apt_cache_add(*args: str)                             -> None: return safe_execute(["apt-cache", "add", *args])
def apt_cache_depends(*args: str)                         -> None: return safe_execute(["apt-cache", "depends", *args])
def apt_cache_dotty(*args: str)                           -> None: return safe_execute(["apt-cache", "dotty", *args])
def apt_cache_dump(*args: str)                            -> None: return safe_execute(["apt-cache", "dump", *args])
def apt_cache_dumpavail(*args: str)                       -> None: return safe_execute(["apt-cache", "dumpavail", *args])
def apt_cache_gencaches(*args: str)                       -> None: return safe_execute(["apt-cache", "gencaches", *args])
def apt_cache_madison(*args: str)                         -> None: return safe_execute(["apt-cache", "madison", *args])
def apt_cache_pkgnames(*args: str)                        -> None: return safe_execute(["apt-cache", "pkgnames", *args])
def apt_cache_policy(*args: str)                          -> None: return safe_execute(["apt-cache", "policy", *args])
def apt_cache_rdepends(*args: str)                        -> None: return safe_execute(["apt-cache", "rdepends", *args])
def apt_cache_search(*args: str)                          -> None: return safe_execute(["apt-cache", "search", *args])
def apt_cache_show(*args: str)                            -> None: return safe_execute(["apt-cache", "show", *args])
def apt_cache_showpkg(*args: str)                         -> None: return safe_execute(["apt-cache", "showpkg", *args])
def apt_cache_showsrc(*args: str)                         -> None: return safe_execute(["apt-cache", "showsrc", *args])
def apt_cache_stats(*args: str)                           -> None: return safe_execute(["apt-cache", "stats", *args])
def apt_cache_unmet(*args: str)                           -> None: return safe_execute(["apt-cache", "unmet", *args])
def apt_cache_xvcg(*args: str)                            -> None: return safe_execute(["apt-cache", "xvcg", *args])
#
# `apt-cdrom`:
#
def apt_cdrom(*args: str)                                 -> None: return safe_execute(["apt-cdrom", *args])
def apt_cdrom_add(*args: str)                             -> None: return safe_execute(["apt-cdrom", "add", *args])
def apt_cdrom_ident(*args: str)                           -> None: return safe_execute(["apt-cdrom", "ident", *args])
#
# `apt-config`:
#
def apt_config(*args: str)                                -> None: return safe_execute(["apt-config", *args])
def apt_config_shell(*args: str)                          -> None: return safe_execute(["apt-config", "shell", *args])
def apt_config_dump(*args: str)                           -> None: return safe_execute(["apt-config", "dump", *args])
#
# `apt-extracttemplates`:
#
def apt_extracttemplates(*args: str)                      -> None: return safe_execute(["apt-extracttemplates", *args])
#
# `apt-get`:
#
def apt_get(*args: str)                                   -> None: return safe_execute(["apt-get", *args])
def apt_get_autoclean(*args: str)                         -> None: return safe_execute(["apt-get", "autoclean", *args])
def apt_get_build_dep(*args: str)                         -> None: return safe_execute(["apt-get", "build-dep", *args])
def apt_get_check(*args: str)                             -> None: return safe_execute(["apt-get", "check", *args])
def apt_get_dist_upgrade(*args: str)                      -> None: return safe_execute(["apt-get", "dist-upgrade", *args])
def apt_get_dselect_upgrade(*args: str)                   -> None: return safe_execute(["apt-get", "dselect-upgrade", *args])
def apt_get_install(*args: str)                           -> None: return safe_execute(["apt-get", "install", *args])
def apt_get_remove(*args: str)                            -> None: return safe_execute(["apt-get", "remove", *args])
def apt_get_update(*args: str)                            -> None: return safe_execute(["apt-get", "update", *args])
def apt_get_autoremove(*args: str)                        -> None: return safe_execute(["apt-get", "autoremove", *args])
def apt_get_changelog(*args: str)                         -> None: return safe_execute(["apt-get", "changelog", *args])
def apt_get_clean(*args: str)                             -> None: return safe_execute(["apt-get", "clean", *args])
def apt_get_download(*args: str)                          -> None: return safe_execute(["apt-get", "download", *args])
def apt_get_indextargets(*args: str)                      -> None: return safe_execute(["apt-get", "indextargets", *args])
def apt_get_purge(*args: str)                             -> None: return safe_execute(["apt-get", "purge", *args])
def apt_get_source(*args: str)                            -> None: return safe_execute(["apt-get", "source", *args])
def apt_get_upgrade(*args: str)                           -> None: return safe_execute(["apt-get", "upgrade", *args])
#
# `apt-listchanges`:
#
def apt_listchanges(*args: str)                           -> None: return safe_execute(["apt-listchanges", *args])
#
# `apt-mark`:
#
def apt_mark(*args: str)                                  -> None: return safe_execute(["apt-mark", *args])
def apt_mark_auto(*args: str)                             -> None: return safe_execute(["apt-mark", "auto", *args])
def apt_mark_manual(*args: str)                           -> None: return safe_execute(["apt-mark", "manual", *args])
def apt_mark_minimize_manual(*args: str)                  -> None: return safe_execute(["apt-mark", "minimize-manual", *args])
def apt_mark_showauto(*args: str)                         -> None: return safe_execute(["apt-mark", "showauto", *args])
def apt_mark_showmanual(*args: str)                       -> None: return safe_execute(["apt-mark", "showmanual", *args])
def apt_mark_hold(*args: str)                             -> None: return safe_execute(["apt-mark", "hold", *args])
def apt_mark_unhold(*args: str)                           -> None: return safe_execute(["apt-mark", "unhold", *args])
def apt_mark_showhold(*args: str)                         -> None: return safe_execute(["apt-mark", "showhold", *args])
#
# `apt-sortpkgs`:
#
def apt_sortpkgs(*args: str)                              -> None: return safe_execute(["apt-sortpkgs", *args])
#
# `aptitude`:
#
def aptitude(*args: str)                                  -> None: return safe_execute(["aptitude", *args])
def aptitude_add_user_tag(*args: str)                     -> None: return safe_execute(["aptitude", "add-user-tag", *args])
def aptitude_clean(*args: str)                            -> None: return safe_execute(["aptitude", "clean", *args])
def aptitude_forget_new(*args: str)                       -> None: return safe_execute(["aptitude", "forget-new", *args])
def aptitude_keep(*args: str)                             -> None: return safe_execute(["aptitude", "keep", *args])
def aptitude_reinstall(*args: str)                        -> None: return safe_execute(["aptitude", "reinstall", *args])
def aptitude_search(*args: str)                           -> None: return safe_execute(["aptitude", "search", *args])
def aptitude_update(*args: str)                           -> None: return safe_execute(["aptitude", "update", *args])
def aptitude_why_not(*args: str)                          -> None: return safe_execute(["aptitude", "why-not", *args])
def aptitude_autoclean(*args: str)                        -> None: return safe_execute(["aptitude", "autoclean", *args])
def aptitude_dist_upgrade(*args: str)                     -> None: return safe_execute(["aptitude", "dist-upgrade", *args])
def aptitude_full_upgrade(*args: str)                     -> None: return safe_execute(["aptitude", "full-upgrade", *args])
def aptitude_keep_all(*args: str)                         -> None: return safe_execute(["aptitude", "keep-all", *args])
def aptitude_remove(*args: str)                           -> None: return safe_execute(["aptitude", "remove", *args])
def aptitude_show(*args: str)                             -> None: return safe_execute(["aptitude", "show", *args])
def aptitude_upgrade(*args: str)                          -> None: return safe_execute(["aptitude", "upgrade", *args])
def aptitude_build_dep(*args: str)                        -> None: return safe_execute(["aptitude", "build-dep", *args])
def aptitude_download(*args: str)                         -> None: return safe_execute(["aptitude", "download", *args])
def aptitude_hold(*args: str)                             -> None: return safe_execute(["aptitude", "hold", *args])
def aptitude_markauto(*args: str)                         -> None: return safe_execute(["aptitude", "markauto", *args])
def aptitude_remove_user_tag(*args: str)                  -> None: return safe_execute(["aptitude", "remove-user-tag", *args])
def aptitude_unhold(*args: str)                           -> None: return safe_execute(["aptitude", "unhold", *args])
def aptitude_versions(*args: str)                         -> None: return safe_execute(["aptitude", "versions", *args])
def aptitude_changelog(*args: str)                        -> None: return safe_execute(["aptitude", "changelog", *args])
def aptitude_forbid_version(*args: str)                   -> None: return safe_execute(["aptitude", "forbid-version", *args])
def aptitude_install(*args: str)                          -> None: return safe_execute(["aptitude", "install", *args])
def aptitude_purge(*args: str)                            -> None: return safe_execute(["aptitude", "purge", *args])
def aptitude_safe_upgrade(*args: str)                     -> None: return safe_execute(["aptitude", "safe-upgrade", *args])
def aptitude_unmarkauto(*args: str)                       -> None: return safe_execute(["aptitude", "unmarkauto", *args])
def aptitude_why(*args: str)                              -> None: return safe_execute(["aptitude", "why", *args])
#
# `aptitude-create-state-bundle`:
#
def aptitude_create_state_bundle(*args: str)              -> None: return safe_execute(["aptitude-create-state-bundle", *args])
def aptitude_create_state_bundle_help(*args: str)         -> None: return safe_execute(["aptitude-create-state-bundle", "--help", *args])
def aptitude_create_state_bundle_print_inputs(*args: str) -> None: return safe_execute(["aptitude-create-state-bundle", "--print-inputs", *args])
def aptitude_create_state_bundle_force_bzip2(*args: str)  -> None: return safe_execute(["aptitude-create-state-bundle", "--force-bzip2", *args])
def aptitude_create_state_bundle_force_gzip(*args: str)   -> None: return safe_execute(["aptitude-create-state-bundle", "--force-gzip", *args])
#
# `aptitude-run-state-bundle`:
#
def aptitude_run_state_bundle(*args: str)                 -> None: return safe_execute(["aptitude-run-state-bundle", *args])
#
# `dnf`:
#
def dnf(*args: str)                                       -> None: return safe_execute(["dnf", *args])
def dnf_advisory(*args: str)                              -> None: return safe_execute(["dnf", "advisory", *args])
def dnf_autoremove(*args: str)                            -> None: return safe_execute(["dnf", "autoremove", *args])
def dnf_check(*args: str)                                 -> None: return safe_execute(["dnf", "check", *args])
def dnf_check_upgrade(*args: str)                         -> None: return safe_execute(["dnf", "check-upgrade", *args])
def dnf_clean(*args: str)                                 -> None: return safe_execute(["dnf", "clean", *args])
def dnf_distro_sync(*args: str)                           -> None: return safe_execute(["dnf", "distro-sync", *args])
def dnf_downgrade(*args: str)                             -> None: return safe_execute(["dnf", "downgrade", *args])
def dnf_download(*args: str)                              -> None: return safe_execute(["dnf", "download", *args])
def dnf_environment(*args: str)                           -> None: return safe_execute(["dnf", "environment", *args])
def dnf_group(*args: str)                                 -> None: return safe_execute(["dnf", "group", *args])
def dnf_history(*args: str)                               -> None: return safe_execute(["dnf", "history", *args])
def dnf_info(*args: str)                                  -> None: return safe_execute(["dnf", "info", *args])
def dnf_install(*args: str)                               -> None: return safe_execute(["dnf", "install", *args])
def dnf_leaves(*args: str)                                -> None: return safe_execute(["dnf", "leaves", *args])
def dnf_list(*args: str)                                  -> None: return safe_execute(["dnf", "list", *args])
def dnf_makecache(*args: str)                             -> None: return safe_execute(["dnf", "makecache", *args])
def dnf_mark(*args: str)                                  -> None: return safe_execute(["dnf", "mark", *args])
def dnf_module(*args: str)                                -> None: return safe_execute(["dnf", "module", *args])
def dnf_offline(*args: str)                               -> None: return safe_execute(["dnf", "offline", *args])
def dnf_provides(*args: str)                              -> None: return safe_execute(["dnf", "provides", *args])
def dnf_reinstall(*args: str)                             -> None: return safe_execute(["dnf", "reinstall", *args])
def dnf_remove(*args: str)                                -> None: return safe_execute(["dnf", "remove", *args])
def dnf_replay(*args: str)                                -> None: return safe_execute(["dnf", "replay", *args])
def dnf_repo(*args: str)                                  -> None: return safe_execute(["dnf", "repo", *args])
def dnf_repoquery(*args: str)                             -> None: return safe_execute(["dnf", "repoquery", *args])
def dnf_search(*args: str)                                -> None: return safe_execute(["dnf", "search", *args])
def dnf_swap(*args: str)                                  -> None: return safe_execute(["dnf", "swap", *args])
def dnf_system_upgrade(*args: str)                        -> None: return safe_execute(["dnf", "system-upgrade", *args])
def dnf_upgrade(*args: str)                               -> None: return safe_execute(["dnf", "upgrade", *args])
def dnf_versionlock(*args: str)                           -> None: return safe_execute(["dnf", "versionlock", *args])
def dnf_debuginfo_install(*args: str)                     -> None: return safe_execute(["dnf", "debuginfo-install", *args])
def dnf_offline_distrosync(*args: str)                    -> None: return safe_execute(["dnf", "offline-distrosync", *args])
def dnf_offline_upgrade(*args: str)                       -> None: return safe_execute(["dnf", "offline-upgrade", *args])
def dnf_config_manager(*args: str)                        -> None: return safe_execute(["dnf", "config-manager", *args])
def dnf_builddep(*args: str)                              -> None: return safe_execute(["dnf", "builddep", *args])
def dnf_changelog(*args: str)                             -> None: return safe_execute(["dnf", "changelog", *args])
def dnf_copr(*args: str)                                  -> None: return safe_execute(["dnf", "copr", *args])
def dnf_needs_restarting(*args: str)                      -> None: return safe_execute(["dnf", "needs-restarting", *args])
def dnf_repoclosure(*args: str)                           -> None: return safe_execute(["dnf", "repoclosure", *args])
def dnf_reposync(*args: str)                              -> None: return safe_execute(["dnf", "reposync", *args])
#
# `dpkg`:
#
def dpkg(*args: str)                                      -> None: return safe_execute(["dpkg", *args])
def dpkg_abort_after(*args: str)                          -> None: return safe_execute(["dpkg", "--abort-after", *args])
def dpkg_add_architecture(*args: str)                     -> None: return safe_execute(["dpkg", "--add-architecture", *args])
def dpkg_audit(*args: str)                                -> None: return safe_execute(["dpkg", "--audit", *args])
def dpkg_auto_deconfigure(*args: str)                     -> None: return safe_execute(["dpkg", "--auto-deconfigure", *args])
def dpkg_clear_avail(*args: str)                          -> None: return safe_execute(["dpkg", "--clear-avail", *args])
def dpkg_clear_selection(*args: str)                      -> None: return safe_execute(["dpkg", "--clear-selections", *args])
def dpkg_compare_versions(*args: str)                     -> None: return safe_execute(["dpkg", "--compare-versions", *args])
def dpkg_configure(*args: str)                            -> None: return safe_execute(["dpkg", "--configure", *args])
def dpkg_field(*args: str)                                -> None: return safe_execute(["dpkg", "--field", *args])
def dpkg_forget_old_unavail(*args: str)                   -> None: return safe_execute(["dpkg", "--forget-old-unavail", *args])
def dpkg_get_selections(*args: str)                       -> None: return safe_execute(["dpkg", "--get-selections", *args])
def dpkg_help(*args: str)                                 -> None: return safe_execute(["dpkg", "--help", *args])
def dpkg_install(*args: str)                              -> None: return safe_execute(["dpkg", "--install", *args])
def dpkg_list(*args: str)                                 -> None: return safe_execute(["dpkg", "--list", *args])
def dpkg_listfiles(*args: str)                            -> None: return safe_execute(["dpkg", "--listfiles", *args])
def dpkg_merge_avail(*args: str)                          -> None: return safe_execute(["dpkg", "--merge-avail", *args])
def dpkg_predep_package(*args: str)                       -> None: return safe_execute(["dpkg", "--predep-package", *args])
def dpkg_print_architecture(*args: str)                   -> None: return safe_execute(["dpkg", "--print-architecture", *args])
def dpkg_print_avail(*args: str)                          -> None: return safe_execute(["dpkg", "--print-avail", *args])
def dpkg_print_foreign_architectures(*args: str)          -> None: return safe_execute(["dpkg", "--print-foreign-architectures", *args])
def dpkg_purge(*args: str)                                -> None: return safe_execute(["dpkg", "--purge", *args])
def dpkg_record_avail(*args: str)                         -> None: return safe_execute(["dpkg", "--record-avail", *args])
def dpkg_remove(*args: str)                               -> None: return safe_execute(["dpkg", "--remove", *args])
def dpkg_remove_architecture(*args: str)                  -> None: return safe_execute(["dpkg", "--remove-architecture", *args])
def dpkg_search(*args: str)                               -> None: return safe_execute(["dpkg", "--search", *args])
def dpkg_set_selections(*args: str)                       -> None: return safe_execute(["dpkg", "--set-selections", *args])
def dpkg_status(*args: str)                               -> None: return safe_execute(["dpkg", "--status", *args])
def dpkg_unpack(*args: str)                               -> None: return safe_execute(["dpkg", "--unpack", *args])
def dpkg_update_avail(*args: str)                         -> None: return safe_execute(["dpkg", "--update-avail", *args])
def dpkg_verify(*args: str)                               -> None: return safe_execute(["dpkg", "--verify", *args])
def dpkg_version(*args: str)                              -> None: return safe_execute(["dpkg", "--version", *args])
#
# `guix`:
#
def guix(*args: str)                                      -> None: return safe_execute(["guix", *args])
def guix_archive(*args: str)                              -> None: return safe_execute(["guix", "archive", *args])
def guix_build(*args: str)                                -> None: return safe_execute(["guix", "build", *args])
def guix_challenge(*args: str)                            -> None: return safe_execute(["guix", "challenge", *args])
def guix_container(*args: str)                            -> None: return safe_execute(["guix", "container", *args])
def guix_copy(*args: str)                                 -> None: return safe_execute(["guix", "copy", *args])
def guix_deploy(*args: str)                               -> None: return safe_execute(["guix", "deploy", *args])
def guix_describe(*args: str)                             -> None: return safe_execute(["guix", "describe", *args])
def guix_download(*args: str)                             -> None: return safe_execute(["guix", "download", *args])
def guix_edit(*args: str)                                 -> None: return safe_execute(["guix", "edit", *args])
def guix_environment(*args: str)                          -> None: return safe_execute(["guix", "environment", *args])
def guix_gc(*args: str)                                   -> None: return safe_execute(["guix", "gc", *args])
def guix_git(*args: str)                                  -> None: return safe_execute(["guix", "git", *args])
def guix_graph(*args: str)                                -> None: return safe_execute(["guix", "graph", *args])
def guix_hash(*args: str)                                 -> None: return safe_execute(["guix", "hash", *args])
def guix_help(*args: str)                                 -> None: return safe_execute(["guix", "--help", *args])
def guix_home(*args: str)                                 -> None: return safe_execute(["guix", "home", *args])
def guix_import(*args: str)                               -> None: return safe_execute(["guix", "import", *args])
def guix_install(*args: str)                              -> None: return safe_execute(["guix", "install", *args])
def guix_lint(*args: str)                                 -> None: return safe_execute(["guix", "lint", *args])
def guix_offload(*args: str)                              -> None: return safe_execute(["guix", "offload", *args])
def guix_pack(*args: str)                                 -> None: return safe_execute(["guix", "pack", *args])
def guix_package(*args: str)                              -> None: return safe_execute(["guix", "package", *args])
def guix_processes(*args: str)                            -> None: return safe_execute(["guix", "processes", *args])
def guix_publish(*args: str)                              -> None: return safe_execute(["guix", "publish", *args])
def guix_pull(*args: str)                                 -> None: return safe_execute(["guix", "pull", *args])
def guix_refresh(*args: str)                              -> None: return safe_execute(["guix", "refresh", *args])
def guix_remove(*args: str)                               -> None: return safe_execute(["guix", "remove", *args])
def guix_repl(*args: str)                                 -> None: return safe_execute(["guix", "repl", *args])
def guix_search(*args: str)                               -> None: return safe_execute(["guix", "search", *args])
def guix_shell(*args: str)                                -> None: return safe_execute(["guix", "shell", *args])
def guix_show(*args: str)                                 -> None: return safe_execute(["guix", "show", *args])
def guix_size(*args: str)                                 -> None: return safe_execute(["guix", "size", *args])
def guix_style(*args: str)                                -> None: return safe_execute(["guix", "style", *args])
def guix_system(*args: str)                               -> None: return safe_execute(["guix", "system", *args])
def guix_time_machine(*args: str)                         -> None: return safe_execute(["guix", "time-machine", *args])
def guix_upgrade(*args: str)                              -> None: return safe_execute(["guix", "upgrade", *args])
def guix_weather(*args: str)                              -> None: return safe_execute(["guix", "weather", *args])
#
# `homebrew`:
#
def brew(*args: str)                                      -> None: return safe_execute(["brew", *args])
def brew_alias(*args: str)                                -> None: return safe_execute(["brew", "alias", *args])
def brew_analytics(*args: str)                            -> None: return safe_execute(["brew", "analytics", *args])
def brew_autoremove(*args: str)                           -> None: return safe_execute(["brew", "autoremove", *args])
def brew_bundle(*args: str)                               -> None: return safe_execute(["brew", "bundle", *args])
def brew_casks(*args: str)                                -> None: return safe_execute(["brew", "casks", *args])
def brew_cleanup(*args: str)                              -> None: return safe_execute(["brew", "cleanup", *args])
def brew_command(*args: str)                              -> None: return safe_execute(["brew", "command", *args])
def brew_commands(*args: str)                             -> None: return safe_execute(["brew", "commands", *args])
def brew_completions(*args: str)                          -> None: return safe_execute(["brew", "completions", *args])
def brew_config(*args: str)                               -> None: return safe_execute(["brew", "config", *args])
def brew_deps(*args: str)                                 -> None: return safe_execute(["brew", "deps", *args])
def brew_desc(*args: str)                                 -> None: return safe_execute(["brew", "desc", *args])
def brew_developer(*args: str)                            -> None: return safe_execute(["brew", "developer", *args])
def brew_docs(*args: str)                                 -> None: return safe_execute(["brew", "docs", *args])
def brew_fetch(*args: str)                                -> None: return safe_execute(["brew", "fetch", *args])
def brew_formulae(*args: str)                             -> None: return safe_execute(["brew", "formulae", *args])
def brew_gist_logs(*args: str)                            -> None: return safe_execute(["brew", "gist-logs", *args])
def brew_help(*args: str)                                 -> None: return safe_execute(["brew", "help", *args])
def brew_home(*args: str)                                 -> None: return safe_execute(["brew", "home", *args])
def brew_install(*args: str)                              -> None: return safe_execute(["brew", "install", *args])
def brew_leaves(*args: str)                               -> None: return safe_execute(["brew", "leaves", *args])
def brew_link(*args: str)                                 -> None: return safe_execute(["brew", "link", *args])
def brew_list(*args: str)                                 -> None: return safe_execute(["brew", "list", *args])
def brew_log(*args: str)                                  -> None: return safe_execute(["brew", "log", *args])
def brew_mcp_server(*args: str)                           -> None: return safe_execute(["brew", "mcp-server", *args])
def brew_migrate(*args: str)                              -> None: return safe_execute(["brew", "migrate", *args])
def brew_missing(*args: str)                              -> None: return safe_execute(["brew", "missing", *args])
def brew_nodenv_sync(*args: str)                          -> None: return safe_execute(["brew", "nodenv-sync", *args])
def brew_options(*args: str)                              -> None: return safe_execute(["brew", "options", *args])
def brew_outdated(*args: str)                             -> None: return safe_execute(["brew", "outdated", *args])
def brew_pin(*args: str)                                  -> None: return safe_execute(["brew", "pin", *args])
def brew_postinstall(*args: str)                          -> None: return safe_execute(["brew", "postinstall", *args])
def brew_pyenv_sync(*args: str)                           -> None: return safe_execute(["brew", "pyenv-sync", *args])
def brew_rbenv_sync(*args: str)                           -> None: return safe_execute(["brew", "rbenv-sync", *args])
def brew_readall(*args: str)                              -> None: return safe_execute(["brew", "readall", *args])
def brew_reinstall(*args: str)                            -> None: return safe_execute(["brew", "reinstall", *args])
def brew_search(*args: str)                               -> None: return safe_execute(["brew", "search", *args])
def brew_services(*args: str)                             -> None: return safe_execute(["brew", "services", *args])
def brew_setup_ruby(*args: str)                           -> None: return safe_execute(["brew", "setup-ruby", *args])
def brew_shellenv(*args: str)                             -> None: return safe_execute(["brew", "shellenv", *args])
def brew_tab(*args: str)                                  -> None: return safe_execute(["brew", "tab", *args])
def brew_tap(*args: str)                                  -> None: return safe_execute(["brew", "tap", *args])
def brew_tap_info(*args: str)                             -> None: return safe_execute(["brew", "tap-info", *args])
def brew_unalias(*args: str)                              -> None: return safe_execute(["brew", "unalias", *args])
def brew_uninstall(*args: str)                            -> None: return safe_execute(["brew", "uninstall", *args])
def brew_unlink(*args: str)                               -> None: return safe_execute(["brew", "unlink", *args])
def brew_unpin(*args: str)                                -> None: return safe_execute(["brew", "unpin", *args])
def brew_untap(*args: str)                                -> None: return safe_execute(["brew", "untap", *args])
def brew_update(*args: str)                               -> None: return safe_execute(["brew", "update", *args])
def brew_update_if_needed(*args: str)                     -> None: return safe_execute(["brew", "update-if-needed", *args])
def brew_update_reset(*args: str)                         -> None: return safe_execute(["brew", "update-reset", *args])
def brew_upgrade(*args: str)                              -> None: return safe_execute(["brew", "upgrade", *args])
def brew_uses(*args: str)                                 -> None: return safe_execute(["brew", "uses", *args])
def brew_cache(*args: str)                                -> None: return safe_execute(["brew", "--cache", *args])
def brew_caskroom(*args: str)                             -> None: return safe_execute(["brew", "--caskroom", *args])
def brew_cellar(*args: str)                               -> None: return safe_execute(["brew", "--cellar", *args])
def brew_env(*args: str)                                  -> None: return safe_execute(["brew", "--env", *args])
def brew_prefix(*args: str)                               -> None: return safe_execute(["brew", "--prefix", *args])
def brew_repository(*args: str)                           -> None: return safe_execute(["brew", "--repository", *args])
def brew_version(*args: str)                              -> None: return safe_execute(["brew", "--version", *args])
#
# `pacman`:
#
def pacman(*args: str)                                    -> None: return safe_execute(["pacman", *args])
def pacman_help(*args: str)                               -> None: return safe_execute(["pacman", "--help", *args])
def pacman_version(*args: str)                            -> None: return safe_execute(["pacman", "--version", *args])
def pacman_database(*args: str)                           -> None: return safe_execute(["pacman", "--database", *args])
def pacman_files(*args: str)                              -> None: return safe_execute(["pacman", "--files", *args])
def pacman_query(*args: str)                              -> None: return safe_execute(["pacman", "--query", *args])
def pacman_remove(*args: str)                             -> None: return safe_execute(["pacman", "--remove", *args])
def pacman_sync(*args: str)                               -> None: return safe_execute(["pacman", "--sync", *args])
def pacman_deptest(*args: str)                            -> None: return safe_execute(["pacman", "--deptest", *args])
def pacman_upgrade(*args: str)                            -> None: return safe_execute(["pacman", "--upgrade", *args])
#
# `pamac`:
#
def pamac(*args: str)                                     -> None: return safe_execute(["pamac", *args])
def pamac_version(*args: str)                             -> None: return safe_execute(["pamac", "--version", *args])
def pamac_help(*args: str)                                -> None: return safe_execute(["pamac", "--help", *args])
def pamac_search(*args: str)                              -> None: return safe_execute(["pamac", "search", *args]) 
def pamac_list(*args: str)                                -> None: return safe_execute(["pamac", "list", *args])
def pamac_info(*args: str)                                -> None: return safe_execute(["pamac", "info", *args])
def pamac_install(*args: str)                             -> None: return safe_execute(["pamac", "install", *args])
def pamac_reinstall(*args: str)                           -> None: return safe_execute(["pamac", "reinstall", *args])
def pamac_remove(*args: str)                              -> None: return safe_execute(["pamac", "remove", *args])
def pamac_checkupdates(*args: str)                        -> None: return safe_execute(["pamac", "checkupdates", *args])
def pamac_upgrade(*args: str)                             -> None: return safe_execute(["pamac", "upgrade", *args])
def pamac_update(*args: str)                              -> None: return safe_execute(["pamac", "update", *args])
def pamac_clone(*args: str)                               -> None: return safe_execute(["pamac", "clone", *args])
def pamac_build(*args: str)                               -> None: return safe_execute(["pamac", "build", *args])
def pamac_clean(*args: str)                               -> None: return safe_execute(["pamac", "clean", *args])
#
# `pkg`:
#
def pkg(*args: str)                                       -> None: safe_execute(["pkg", *args])
def freebsd_pkg_add(*args: str)                           -> None: safe_execute(["pkg", "add", *args])
def pkg_alias(*args: str)                                 -> None: safe_execute(["pkg", "alias", *args])
def pkg_all_depends(*args: str)                           -> None: safe_execute(["pkg", "all-depends", *args])
def pkg_annotate(*args: str)                              -> None: safe_execute(["pkg", "annotate", *args])
def pkg_annotations(*args: str)                           -> None: safe_execute(["pkg", "annotations", *args])
def freebsd_pkg_audit(*args: str)                         -> None: safe_execute(["pkg", "audit", *args])
def pkg_autoremove(*args: str)                            -> None: safe_execute(["pkg", "autoremove", *args])
def pkg_backup(*args: str)                                -> None: safe_execute(["pkg", "backup", *args])
def pkg_bootstrap(*args: str)                             -> None: safe_execute(["pkg", "bootstrap", *args])
def pkg_build_depends(*args: str)                         -> None: safe_execute(["pkg", "build-depends", *args])
def pkg_check(*args: str)                                 -> None: safe_execute(["pkg", "check", *args])
def pkg_cinfo(*args: str)                                 -> None: safe_execute(["pkg", "cinfo", *args])
def pkg_clean(*args: str)                                 -> None: safe_execute(["pkg", "clean", *args])
def pkg_comment(*args: str)                               -> None: safe_execute(["pkg", "comment", *args])
def pkg_convert(*args: str)                               -> None: safe_execute(["pkg", "convert", *args])
def freebsd_pkg_create(*args: str)                        -> None: safe_execute(["pkg", "create", *args])
def pkg_csearch(*args: str)                               -> None: safe_execute(["pkg", "csearch", *args])
def freebsd_pkg_delete(*args: str)                        -> None: safe_execute(["pkg", "delete", *args])
def pkg_desc(*args: str)                                  -> None: safe_execute(["pkg", "desc", *args])
def pkg_download(*args: str)                              -> None: safe_execute(["pkg", "download", *args])
def pkg_fetch(*args: str)                                 -> None: safe_execute(["pkg", "fetch", *args])
def pkg_help(*args: str)                                  -> None: safe_execute(["pkg", "help", *args])
def pkg_iinfo(*args: str)                                 -> None: safe_execute(["pkg", "iinfo", *args])
def freebsd_pkg_info(*args: str)                          -> None: safe_execute(["pkg", "info", *args])
def pkg_install(*args: str)                               -> None: safe_execute(["pkg", "install", *args])
def pkg_isearch(*args: str)                               -> None: safe_execute(["pkg", "isearch", *args])
def pkg_leaf(*args: str)                                  -> None: safe_execute(["pkg", "leaf", *args])
def pkg_list(*args: str)                                  -> None: safe_execute(["pkg", "list", *args])
def pkg_lock(*args: str)                                  -> None: safe_execute(["pkg", "lock", *args])
def pkg_noauto(*args: str)                                -> None: safe_execute(["pkg", "noauto", *args])
def pkg_options(*args: str)                               -> None: safe_execute(["pkg", "options", *args])
def pkg_origin(*args: str)                                -> None: safe_execute(["pkg", "origin", *args])
def pkg_orphans(*args: str)                               -> None: safe_execute(["pkg", "orphans", *args])
def pkg_plugins(*args: str)                               -> None: safe_execute(["pkg", "plugins", *args])
def pkg_prime_list(*args: str)                            -> None: safe_execute(["pkg", "prime-list", *args])
def pkg_prime_origins(*args: str)                         -> None: safe_execute(["pkg", "prime-origins", *args])
def pkg_provided_depends(*args: str)                      -> None: safe_execute(["pkg", "provided-depends", *args])
def pkg_query(*args: str)                                 -> None: safe_execute(["pkg", "query", *args])
def pkg_rall_depends(*args: str)                          -> None: safe_execute(["pkg", "rall-depends", *args])
def pkg_raw(*args: str)                                   -> None: safe_execute(["pkg", "raw", *args])
def pkg_rcomment(*args: str)                              -> None: safe_execute(["pkg", "rcomment", *args])
def pkg_rdesc(*args: str)                                 -> None: safe_execute(["pkg", "rdesc", *args])
def pkg_register(*args: str)                              -> None: safe_execute(["pkg", "register", *args])
def pkg_remove(*args: str)                                -> None: safe_execute(["pkg", "remove", *args])
def pkg_repo(*args: str)                                  -> None: safe_execute(["pkg", "repo", *args])
def pkg_required_depends(*args: str)                      -> None: safe_execute(["pkg", "required-depends", *args])
def pkg_roptions(*args: str)                              -> None: safe_execute(["pkg", "roptions", *args])
def pkg_rquery(*args: str)                                -> None: safe_execute(["pkg", "rquery", *args])
def pkg_runmaintained(*args: str)                         -> None: safe_execute(["pkg", "runmaintained", *args])
def pkg_search(*args: str)                                -> None: safe_execute(["pkg", "search", *args])
def pkg_set(*args: str)                                   -> None: safe_execute(["pkg", "set", *args])
def pkg_shared_depends(*args: str)                        -> None: safe_execute(["pkg", "shared-depends", *args])
def pkg_shell(*args: str)                                 -> None: safe_execute(["pkg", "shell", *args])
def pkg_shlib(*args: str)                                 -> None: safe_execute(["pkg", "shlib", *args])
def pkg_show(*args: str)                                  -> None: safe_execute(["pkg", "show", *args])
def pkg_size(*args: str)                                  -> None: safe_execute(["pkg", "size", *args])
def pkg_stats(*args: str)                                 -> None: safe_execute(["pkg", "stats", *args])
def pkg_unlock(*args: str)                                -> None: safe_execute(["pkg", "unlock", *args])
def pkg_unmaintained(*args: str)                          -> None: safe_execute(["pkg", "unmaintained", *args])
def pkg_update(*args: str)                                -> None: safe_execute(["pkg", "update", *args])
def pkg_updating(*args: str)                              -> None: safe_execute(["pkg", "updating", *args])
def pkg_upgrade(*args: str)                               -> None: safe_execute(["pkg", "upgrade", *args])
def pkg_version(*args: str)                               -> None: safe_execute(["pkg", "version", *args])
def pkg_which(*args: str)                                 -> None: safe_execute(["pkg", "which", *args])
#
# `pkg_add`:
#
def pkg_add(*args: str)                                   -> None: safe_execute(["pkg_add", *args])
#
# `pkg_create`:
#
def pkg_create(*args: str)                                -> None: safe_execute(["pkg_create", *args])
#
# `pkg_delete`:
#
def pkg_delete(*args: str)                                -> None: safe_execute(["pkg_delete", *args])
#
# `pkg_info`:
#
def pkg_info(*args: str)                                  -> None: safe_execute(["pkg_info", *args])
#
# `pkgin`:
#
def pkgin(*args: str)                                     -> None: safe_execute(["pkgin", *args])
def pkgin_list(*args: str)                                -> None: safe_execute(["pkgin", "list", *args])
def pkgin_avail(*args: str)                               -> None: safe_execute(["pkgin", "avail", *args])
def pkgin_search(*args: str)                              -> None: safe_execute(["pkgin", "search", *args])
def pkgin_install(*args: str)                             -> None: safe_execute(["pkgin", "install", *args])
def pkgin_update(*args: str)                              -> None: safe_execute(["pkgin", "update", *args])
def pkgin_upgrade(*args: str)                             -> None: safe_execute(["pkgin", "upgrade", *args])
def pkgin_full_upgrade(*args: str)                        -> None: safe_execute(["pkgin", "full-upgrade", *args])
def pkgin_remove(*args: str)                              -> None: safe_execute(["pkgin", "remove", *args])
def pkgin_keep(*args: str)                                -> None: safe_execute(["pkgin", "keep", *args])
def pkgin_unkeep(*args: str)                              -> None: safe_execute(["pkgin", "unkeep", *args])
def pkgin_export(*args: str)                              -> None: safe_execute(["pkgin", "export", *args])
def pkgin_import(*args: str)                              -> None: safe_execute(["pkgin", "import", *args])
def pkgin_show_keep(*args: str)                           -> None: safe_execute(["pkgin", "show-keep", *args])
def pkgin_show_no_keep(*args: str)                        -> None: safe_execute(["pkgin", "show-no-keep", *args])
def pkgin_autoremove(*args: str)                          -> None: safe_execute(["pkgin", "autoremove", *args])
def pkgin_clean(*args: str)                               -> None: safe_execute(["pkgin", "clean", *args])
def pkgin_show_deps(*args: str)                           -> None: safe_execute(["pkgin", "show-deps", *args])
def pkgin_show_full_deps(*args: str)                      -> None: safe_execute(["pkgin", "show-full-deps", *args])
def pkgin_show_rev_deps(*args: str)                       -> None: safe_execute(["pkgin", "show-rev-deps", *args])
def pkgin_provides(*args: str)                            -> None: safe_execute(["pkgin", "provides", *args])
def pkgin_requires(*args: str)                            -> None: safe_execute(["pkgin", "requires", *args])
def pkgin_show_category(*args: str)                       -> None: safe_execute(["pkgin", "show-category", *args])
def pkgin_show_pkg_category(*args: str)                   -> None: safe_execute(["pkgin", "show-pkg-category", *args])
def pkgin_show_all_categories(*args: str)                 -> None: safe_execute(["pkgin", "show-all-categories", *args])
def pkgin_pkg_content(*args: str)                         -> None: safe_execute(["pkgin", "pkg-content", *args])
def pkgin_pkg_descr(*args: str)                           -> None: safe_execute(["pkgin", "pkg-descr", *args])
def pkgin_pkg_build_defs(*args: str)                      -> None: safe_execute(["pkgin", "pkg-build-defs", *args])
def pkgin_stats(*args: str)                               -> None: safe_execute(["pkgin", "stats", *args])
#
# `portage`:
#
def portage(*args: str)                                   -> None: raise NotImplementedError("open for pull requests")
#
# `qi`:
#
def qi(*args: str)                                        -> None: safe_execute(["qi", *args])
def qi_warn(*args: str)                                   -> None: safe_execute(["qi", "warn", *args])
def qi_install(*args: str)                                -> None: safe_execute(["qi", "install", *args])
def qi_remove(*args: str)                                 -> None: safe_execute(["qi", "remove", *args])
def qi_upgrade(*args: str)                                -> None: safe_execute(["qi", "upgrade", *args])
def qi_extract(*args: str)                                -> None: safe_execute(["qi", "extract", *args])
def qi_create(*args: str)                                 -> None: safe_execute(["qi", "create", *args])
def qi_build(*args: str)                                  -> None: safe_execute(["qi", "build", *args])
def qi_order(*args: str)                                  -> None: safe_execute(["qi", "order", *args])
#
# `slackpkg`:
#
def slackpkg(*args: str)                                  -> None: safe_execute(["slackpkg", *args])
def slackpkg_search(*args: str)                           -> None: safe_execute(["slackpkg", "search", *args])
def slackpkg_install(*args: str)                          -> None: safe_execute(["slackpkg", "install", *args])
def slackpkg_upgrade(*args: str)                          -> None: safe_execute(["slackpkg", "upgrade", *args])
def slackpkg_reinstall(*args: str)                        -> None: safe_execute(["slackpkg", "reinstall", *args])
def slackpkg_remove(*args: str)                           -> None: safe_execute(["slackpkg", "remove", *args])
def slackpkg_blacklist(*args: str)                        -> None: safe_execute(["slackpkg", "blacklist", *args])
def slackpkg_download(*args: str)                         -> None: safe_execute(["slackpkg", "download", *args])
def slackpkg_info(*args: str)                             -> None: safe_execute(["slackpkg", "info", *args])
def slackpkg_clean_system(*args: str)                     -> None: safe_execute(["slackpkg", "clean-system", *args])
def slackpkg_upgrade_all(*args: str)                      -> None: safe_execute(["slackpkg", "upgrade-all", *args])
def slackpkg_install_new(*args: str)                      -> None: safe_execute(["slackpkg", "install-new", *args])
def slackpkg_check_updates(*args: str)                    -> None: safe_execute(["slackpkg", "check-updates", *args])
def slackpkg_update(*args: str)                           -> None: safe_execute(["slackpkg", "update", *args])
#
# `trizen`:
#
def trizen(*args: str)                                    -> None: safe_execute(["trizen", *args])
def trizen_sync(*args: str)                               -> None: safe_execute(["trizen", "--sync", *args])
def trizen_comments(*args: str)                           -> None: safe_execute(["trizen", "--comments", *args])
def trizen_get(*args: str)                                -> None: safe_execute(["trizen", "--get", *args])
def trizen_remove(*args: str)                             -> None: safe_execute(["trizen", "--remove", *args])
def trizen_query(*args: str)                              -> None: safe_execute(["trizen", "--query", *args])
def trizen_files(*args: str)                              -> None: safe_execute(["trizen", "--files", *args])
def trizen_database(*args: str)                           -> None: safe_execute(["trizen", "--database", *args])
def trizen_deptest(*args: str)                            -> None: safe_execute(["trizen", "--deptest", *args])
def trizen_upgrade(*args: str)                            -> None: safe_execute(["trizen", "--upgrade", *args])
#
# `xbps-install`:
#
def xbps_install(*args: str)                              -> None: safe_execute(["xbps-install", *args])
#
# `xbps-query`:
#
def xbps_query(*args: str)                                -> None: safe_execute(["xbps-query", *args])
def xbps_query_list_pkgs(*args: str)                      -> None: safe_execute(["xbps-query", "--list-pkgs", *args])
def xbps_query_list_hold_pkgs(*args: str)                 -> None: safe_execute(["xbps-query", "--list-hold-pkgs", *args])
def xbps_query_list_repos(*args: str)                     -> None: safe_execute(["xbps-query", "--list-repos", *args])
def xbps_query_list_manual_pkgs(*args: str)               -> None: safe_execute(["xbps-query", "--list-manual-pkgs", *args])
def xbps_query_list_orphans(*args: str)                   -> None: safe_execute(["xbps-query", "--list-orphans", *args])
def xbps_query_ownedby(*args: str)                        -> None: safe_execute(["xbps-query", "--ownedby", *args])
def xbps_query_show(*args: str)                           -> None: safe_execute(["xbps-query", "--show", *args])
def xbps_query_search(*args: str)                         -> None: safe_execute(["xbps-query", "--search", *args])
def xbps_query_files(*args: str)                          -> None: safe_execute(["xbps-query", "--files", *args])
def xbps_query_deps(*args: str)                           -> None: safe_execute(["xbps-query", "--deps", *args])
def xbps_query_revdeps(*args: str)                        -> None: safe_execute(["xbps-query", "--revdeps", *args])
def xbps_query_cat(*args: str)                            -> None: safe_execute(["xbps-query", "cat", *args])
#
# `xbps-remove`:
#
def xbps_remove(*args: str)                               -> None: safe_execute(["xbps-install", *args])
#
# `yay`:
#
def yay(*args: str)                                       -> None: safe_execute(["yay", *args])
def yay_build(*args: str)                                 -> None: safe_execute(["yay", "--build", *args])
def yay_show(*args: str)                                  -> None: safe_execute(["yay", "--show", *args])
def yay_getpkgbuild(*args: str)                           -> None: safe_execute(["yay", "--getpkgbuild", *args])
def yay_web(*args: str)                                   -> None: safe_execute(["yay", "--web", *args])
#
# `yum`:
#
def yum(*args: str)                                       -> None: safe_execute(["yum", *args])
def yum_advisory(*args: str)                              -> None: safe_execute(["yum", "advisory", *args])
def yum_autoremove(*args: str)                            -> None: safe_execute(["yum", "autoremove", *args])
def yum_check(*args: str)                                 -> None: safe_execute(["yum", "check", *args])
def yum_check_upgrade(*args: str)                         -> None: safe_execute(["yum", "check-upgrade", *args])
def yum_clean(*args: str)                                 -> None: safe_execute(["yum", "clean", *args])
def yum_distro_sync(*args: str)                           -> None: safe_execute(["yum", "distro-sync", *args])
def yum_downgrade(*args: str)                             -> None: safe_execute(["yum", "downgrade", *args])
def yum_download(*args: str)                              -> None: safe_execute(["yum", "download", *args])
def yum_environment(*args: str)                           -> None: safe_execute(["yum", "environment", *args])
def yum_group(*args: str)                                 -> None: safe_execute(["yum", "group", *args])
def yum_history(*args: str)                               -> None: safe_execute(["yum", "history", *args])
def yum_info(*args: str)                                  -> None: safe_execute(["yum", "info", *args])
def yum_install(*args: str)                               -> None: safe_execute(["yum", "install", *args])
def yum_leaves(*args: str)                                -> None: safe_execute(["yum", "leaves", *args])
def yum_list(*args: str)                                  -> None: safe_execute(["yum", "list", *args])
def yum_makecache(*args: str)                             -> None: safe_execute(["yum", "makecache", *args])
def yum_mark(*args: str)                                  -> None: safe_execute(["yum", "mark", *args])
def yum_module(*args: str)                                -> None: safe_execute(["yum", "module", *args])
def yum_offline(*args: str)                               -> None: safe_execute(["yum", "offline", *args])
def yum_provides(*args: str)                              -> None: safe_execute(["yum", "provides", *args])
def yum_reinstall(*args: str)                             -> None: safe_execute(["yum", "reinstall", *args])
def yum_remove(*args: str)                                -> None: safe_execute(["yum", "remove", *args])
def yum_replay(*args: str)                                -> None: safe_execute(["yum", "replay", *args])
def yum_repo(*args: str)                                  -> None: safe_execute(["yum", "repo", *args])
def yum_repoquery(*args: str)                             -> None: safe_execute(["yum", "repoquery", *args])
def yum_search(*args: str)                                -> None: safe_execute(["yum", "search", *args])
def yum_swap(*args: str)                                  -> None: safe_execute(["yum", "swap", *args])
def yum_system_upgrade(*args: str)                        -> None: safe_execute(["yum", "system-upgrade", *args])
def yum_upgrade(*args: str)                               -> None: safe_execute(["yum", "upgrade", *args])
def yum_versionlock(*args: str)                           -> None: safe_execute(["yum", "versionlock", *args])
def yum_debuginfo_install(*args: str)                     -> None: safe_execute(["yum", "debuginfo-install", *args])
def yum_offline_distrosync(*args: str)                    -> None: safe_execute(["yum", "offline-distrosync", *args])
def yum_offline_upgrade(*args: str)                       -> None: safe_execute(["yum", "offline-upgrade", *args])
def yum_config_manager(*args: str)                        -> None: safe_execute(["yum", "config-manager", *args])
def yum_builddep(*args: str)                              -> None: safe_execute(["yum", "builddep", *args])
def yum_changelog(*args: str)                             -> None: safe_execute(["yum", "changelog", *args])
def yum_copr(*args: str)                                  -> None: safe_execute(["yum", "copr", *args])
def yum_needs_restarting(*args: str)                      -> None: safe_execute(["yum", "needs-restarting", *args])
def yum_repoclosure(*args: str)                           -> None: safe_execute(["yum", "repoclosure", *args])
def yum_reposync(*args: str)                              -> None: safe_execute(["yum", "reposync", *args])
#
# `zypper`:
#
def zypper(*args: str)                                    -> None: safe_execute(["zypper", *args])
def zypper_addlocale(*args: str)                          -> None: safe_execute(["zypper", "addlocale", *args])
def zypper_addlock(*args: str)                            -> None: safe_execute(["zypper", "addlock", *args])
def zypper_addrepo(*args: str)                            -> None: safe_execute(["zypper", "addrepo", *args])
def zypper_addservice(*args: str)                         -> None: safe_execute(["zypper", "addservice", *args])
def zypper_appsteam_cache(*args: str)                     -> None: safe_execute(["zypper", "appstream-cache", *args])
def zypper_clean(*args: str)                              -> None: safe_execute(["zypper", "clean", *args])
def zypper_cleanlocks(*args: str)                         -> None: safe_execute(["zypper", "cleanlocks", *args])
def zypper_dist_upgrade(*args: str)                       -> None: safe_execute(["zypper", "dist-upgrade", *args])
def zypper_download(*args: str)                           -> None: safe_execute(["zypper", "download", *args])
def zypper_help(*args: str)                               -> None: safe_execute(["zypper", "help", *args])
def zypper_info(*args: str)                               -> None: safe_execute(["zypper", "info", *args])
def zypper_install(*args: str)                            -> None: safe_execute(["zypper", "install", *args])
def zypper_install_new_recommends(*args: str)             -> None: safe_execute(["zypper", "install-new-recommends", *args])
def zypper_licenses(*args: str)                           -> None: safe_execute(["zypper", "licenses", *args])
def zypper_list_patches(*args: str)                       -> None: safe_execute(["zypper", "list-patches", *args])
def zypper_list_updates(*args: str)                       -> None: safe_execute(["zypper", "list-updates", *args])
def zypper_locales(*args: str)                            -> None: safe_execute(["zypper", "locales", *args])
def zypper_locks(*args: str)                              -> None: safe_execute(["zypper", "locks", *args])
def zypper_modifyrepo(*args: str)                         -> None: safe_execute(["zypper", "modifyrepo", *args])
def zypper_modifyservice(*args: str)                      -> None: safe_execute(["zypper", "modifyservice", *args])
def zypper_needs_rebooting(*args: str)                    -> None: safe_execute(["zypper", "needs-rebooting", *args])
def zypper_packages(*args: str)                           -> None: safe_execute(["zypper", "packages", *args])
def zypper_patch(*args: str)                              -> None: safe_execute(["zypper", "patch", *args])
def zypper_patch_check(*args: str)                        -> None: safe_execute(["zypper", "patch-check", *args])
def zypper_patches(*args: str)                            -> None: safe_execute(["zypper", "patches", *args])
def zypper_patch_info(*args: str)                         -> None: safe_execute(["zypper", "patch-info", *args])
def zypper_patterns(*args: str)                           -> None: safe_execute(["zypper", "patterns", *args])
def zypper_product_info(*args: str)                       -> None: safe_execute(["zypper", "product-info", *args])
def zypper_products(*args: str)                           -> None: safe_execute(["zypper", "products", *args])
def zypper_purge_kernels(*args: str)                      -> None: safe_execute(["zypper", "purge-kernels", *args])
def zypper_ps(*args: str)                                 -> None: safe_execute(["zypper", "ps", *args])
def zypper_refresh(*args: str)                            -> None: safe_execute(["zypper", "refresh", *args])
def zypper_refresh_services(*args: str)                   -> None: safe_execute(["zypper", "refresh-services", *args])
def zypper_remove(*args: str)                             -> None: safe_execute(["zypper", "remove", *args])
def zypper_removelocale(*args: str)                       -> None: safe_execute(["zypper", "removelocale", *args])
def zypper_removelock(*args: str)                         -> None: safe_execute(["zypper", "removelock", *args])
def zypper_removeptf(*args: str)                          -> None: safe_execute(["zypper", "removeptf", *args])
def zypper_removerepo(*args: str)                         -> None: safe_execute(["zypper", "removerepo", *args])
def zypper_removeservice(*args: str)                      -> None: safe_execute(["zypper", "removeservice", *args])
def zypper_renamerepo(*args: str)                         -> None: safe_execute(["zypper", "renamerepo", *args])
def zypper_repos(*args: str)                              -> None: safe_execute(["zypper", "repos", *args])
def zypper_search(*args: str)                             -> None: safe_execute(["zypper", "search", *args])
def zypper_services(*args: str)                           -> None: safe_execute(["zypper", "services", *args])
def zypper_shell(*args: str)                              -> None: safe_execute(["zypper", "shell", *args])
def zypper_source_download(*args: str)                    -> None: safe_execute(["zypper", "source-download", *args])
def zypper_source_install(*args: str)                     -> None: safe_execute(["zypper", "source-install", *args])
def zypper_subcommand(*args: str)                         -> None: safe_execute(["zypper", "subcommand", *args])
def zypper_system_architecture(*args: str)                -> None: safe_execute(["zypper", "system-architecture", *args])
def zypper_targetos(*args: str)                           -> None: safe_execute(["zypper", "targetos", *args])
def zypper_update(*args: str)                             -> None: safe_execute(["zypper", "update", *args])
def zypper_versioncmp(*args: str)                         -> None: safe_execute(["zypper", "versioncmp", *args])
def zypper_verify(*args: str)                             -> None: safe_execute(["zypper", "verify", *args])
def zypper_what_provides(*args: str)                      -> None: safe_execute(["zypper", "what-provides", *args])
#
# `zypper-log`:
#
def zypper_log(*args: str)                                -> None: safe_execute(["zypper-log", *args])
