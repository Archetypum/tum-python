#!/usr/bin/env python3
#
# `theunixmanager/initmanagement.py`
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

import typing
import subprocess


class Colors:
    RED: str = "\033[0;31m"
    GREEN: str = "\033[0;32m"
    RESET: str = "\033[0m"


class Dinit:
    allowed_commands: typing.Dict[str, typing.Callable[[typing.Optional[str]], bool]]

    def __init__(self) -> None:
        self.allowed_commands = {
            "start": self.start,
            "stop": self.stop,
            "status": self.status,
            "is-started": self.is_started,
            "is-failed": self.is_failed,
            "restart": self.restart,
            "wake": self.wake,
            "release": self.release,
            "unpin": self.unpin,
            "unload": self.unload,
            "reload": self.reload,
            "list": self.list,
            "shutdown": self.shutdown,
            "add-dep": self.add_dep,
            "rm-dep": self.rm_dep,
            "enable": self.enable,
            "disable": self.disable,
            "trigger": self.trigger,
            "untrigger": self.untrigger,
            "setenv": self.setenv,
            "unsetenv": self.unsetenv,
            "catalog": self.catalog,
            "signal": self.signal,
        }

    def _run(self, action: str, service: typing.Optional[str] = None) -> bool:
        cmd: typing.List[str]
        
        cmd = ["dinitctl", action]
        if service:
            cmd.append(service)

        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            print(f"{Colors.GREEN}[*] Success!{Colors.RESET}")
            return True
        except subprocess.CalledProcessError:
            print(f"{Colors.RED}[!] Error: dinitctl {action} {service or ''} failed.{Colors.RESET}")
            return False

    def start(self, service: typing.Optional[str]) -> bool:
        return self._run("start", service)

    def stop(self, service: typing.Optional[str]) -> bool:
        return self._run("stop", service)

    def status(self, service: typing.Optional[str]) -> bool:
        return self._run("status", service)

    def is_started(self, service: typing.Optional[str]) -> bool:
        return self._run("is-started", service)

    def is_failed(self, service: typing.Optional[str]) -> bool:
        return self._run("is-failed", service)

    def restart(self, service: typing.Optional[str]) -> bool:
        return self._run("restart", service)

    def wake(self, service: typing.Optional[str]) -> bool:
        return self._run("wake", service)

    def release(self, service: typing.Optional[str]) -> bool:
        return self._run("release", service)

    def unpin(self, service: typing.Optional[str]) -> bool:
        return self._run("unpin", service)

    def unload(self, service: typing.Optional[str]) -> bool:
        return self._run("unload", service)

    def reload(self, service: typing.Optional[str]) -> bool:
        return self._run("reload", service)

    def list(self, service: typing.Optional[str]) -> bool:
        return self._run("list", service)

    def shutdown(self, service: typing.Optional[str]) -> bool:
        return self._run("shutdown", service)

    def add_dep(self, service: typing.Optional[str]) -> bool:
        return self._run("add-dep", service)

    def rm_dep(self, service: typing.Optional[str]) -> bool:
        return self._run("rm-dep", service)

    def enable(self, service: typing.Optional[str]) -> bool:
        return self._run("enable", service)

    def disable(self, service: typing.Optional[str]) -> bool:
        return self._run("disable", service)
    
    def trigger(self, service: typing.Optional[str]) -> bool:
        return self._run("trigger", service)

    def untrigger(self, service: typing.Optional[str]) -> bool: 
        return self._run("untrigger", service)
        
    def setenv(self, service: typing.Optional[str]) -> bool:
        return self._run("setenv", service)

    def unsetenv(self, service: typing.Optional[str]) -> bool:
        return self._run("unsetenv", service)

    def catalog(self, service: typing.Optional[str]) -> bool:
        return self._run("catalog", service)

    def signal(self, service: typing.Optional[str]) -> bool:
        return self._run("signal", service)

    def execute(self, command: str, service: typing.Optional[str] = None) -> bool:
        handler: typing.Optional[typing.Callable[[str], bool]]

        handler = self.allowed_commands.get(command)
        if handler is None:
            print(f"{Colors.RED}[!] Error: Unsupported command: {command}{Colors.RESET}")
            return False

        return handler(service)


class Launchd:
    ...


class OpenRC:
    allowed_commands: typing.Dict[str, typing.Callable[[str], bool]]

    def __init__(self) -> None:
        self.allowed_commands = {
            "start": self.start,
            "stop": self.stop,
            "restart": self.restart,
            "reload": self.reload,
            "force-reload": self.force_reload,
            "try-restart": self.try_restart,
            "status": self.status,
        }

    def _run(self, action: str, service: str) -> bool:
        cmd: typing.List[str] 

        cmd = ["rc-service", service, action]

        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            print(f"{Colors.GREEN}[*] Success!{Colors.RESET}")
            return True
        except subprocess.CalledProcessError:
            print(f"{Colors.RED}[!] Error: 'rc-service {service} {action}' failed.{Colors.RESET}")
            return False

    def start(self, service: str) -> bool:
        return self._run("start", service)

    def stop(self, service: str) -> bool:
        return self._run("stop", service)

    def restart(self, service: str) -> bool:
        return self._run("restart", service)

    def reload(self, service: str) -> bool:
        return self._run("reload", service)

    def force_reload(self, service: str) -> bool:
        return self._run("force-reload", service)

    def try_restart(self, service: str) -> bool:
        return self._run("try-restart", service)

    def status(self, service: str) -> bool:
        return self._run("status", service)

    def execute(self, command: str, service: str) -> bool:
        handler: typing.Optional[typing.Callable[[str], bool]]

        handler = self.allowed_commands.get(command)
        if handler is None:
            print(f"{Colors.RED}[!] Error: Unsupported command: {command}{Colors.RESET}")
            return False

        return handler(service)


class Runit:
    ...


class S6:
    allowed_commands: typing.Dict[str, typing.Callable[[typing.Optional[str]], bool]]

    def __init__(self) -> None:
        self.allowed_commands = {
            "help": self.help,
            "list": self.list,
            "listall": self.listall,
            "diff": self.diff,
            "start": self.start,
            "stop": self.stop,
            "change": self.change,
        }

    def _run(self, action: str, service: typing.Optional[str] = None) -> bool:
        cmd: typing.List[str] 
        
        cmd = ["s6-rc", action]
        if service:
            cmd.append(service)

        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            print(f"{Colors.GREEN}[*] Success!{Colors.RESET}")
            return True
        except subprocess.CalledProcessError:
            print(f"{Colors.RED}[!] Error: 's6-rc {action} {service or ''}' failed.{Colors.RESET}")
            return False

    def help(self, service: typing.Optional[str] = None) -> bool:
        return self._run("help", service)

    def list(self, service: typing.Optional[str] = None) -> bool:
        return self._run("list", service)

    def listall(self, service: typing.Optional[str] = None) -> bool:
        return self._run("listall", service)

    def diff(self, service: typing.Optional[str] = None) -> bool:
        return self._run("diff", service)

    def start(self, service: typing.Optional[str] = None) -> bool:
        return self._run("start", service)

    def stop(self, service: typing.Optional[str] = None) -> bool:
        return self._run("stop", service)

    def change(self, service: typing.Optional[str] = None) -> bool:
        return self._run("change", service)

    def execute(self, command: str, service: typing.Optional[str] = None) -> bool:
        handler: typing.Optional[typing.Callable[[str], bool]]

        handler = self.allowed_commands.get(command)
        if handler is None:
            print(f"{Colors.RED}[!] Error: Unsupported command: {command}{Colors.RESET}")
            return False
        
        return handler(service)


class Systemd:
    ...


class SysVinit:
    ...
