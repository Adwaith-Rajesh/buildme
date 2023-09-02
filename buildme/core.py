import shlex
import sys
from argparse import Namespace
from functools import wraps
from subprocess import Popen
from typing import Any
from typing import Callable
from typing import NamedTuple


class CommandRunner:
    def __init__(self, shell: bool = False, print_cmd: bool = True,
                 exit_non_zero: bool = True, print_cmd_sep: bool = True) -> None:
        self.shell = shell
        self.print_cmd = print_cmd
        self.exit_non_zero = exit_non_zero
        self.print_cmd_sep = print_cmd_sep

    def run(self, cmd: str) -> int:
        if self.print_cmd_sep:
            print('=' * 80)

        if self.print_cmd:
            print(f'[CMD]: {cmd}')

        p = Popen(args=shlex.split(cmd), shell=self.shell)
        p.wait()

        if self.print_cmd_sep:
            print('=' * 80)

        if self.exit_non_zero and p.returncode != 0:
            print(f'Last command exited with non zero exit code. [{p.returncode}]')
            exit(1)

        return p.returncode

    def set_exit_non_zero(self, val: bool) -> None:
        self.exit_non_zero = val


class TargetData(NamedTuple):
    name: str
    depends: list[str] = []


TargetFuncType = Callable[[Namespace, TargetData], None]
WrapTargetFuncType = Callable[[Namespace], None]

_targets = {}


def target(depends: list[str] = []) -> Callable[[TargetFuncType], WrapTargetFuncType]:
    def target_dec(fn: TargetFuncType) -> WrapTargetFuncType:
        _targets[fn.__name__] = TargetData(name=fn.__name__, depends=depends)

        @wraps(fn)
        def target_wrap(opts: Namespace) -> None:
            fn(opts, _targets[fn.__name__])
        return target_wrap
    return target_dec


def _get_target_data(name: str) -> TargetData | None:
    return _targets.get(name, None)


def _check_target_exists(name: str) -> bool: return name in _targets


def _exec_target(name: str, opts: Namespace, target_globals: dict[str, Any]) -> None:
    if name not in _targets:
        print(f'unknown target: {name}', file=sys.stderr)
        exit(1)

    if callable(fn := target_globals[name]):
        t_data = _get_target_data(name)
        if t_data:
            for d in t_data.depends:
                _exec_target(d, opts, target_globals)
        fn(opts)
