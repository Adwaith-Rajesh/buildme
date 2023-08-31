import shlex
from subprocess import Popen


class CommandRunner:
    def __init__(self, shell: bool = False, print_cmd: bool = True,
                 exit_non_zero: bool = True, print_cmd_sep: bool = True) -> None:
        self.shell = shell
        self.print_cmd = print_cmd
        self.exit_non_zero = exit_non_zero
        self.print_cmd_sep = print_cmd_sep

    def run(self, cmd: str) -> int:
        if self.print_cmd:
            print('=' * 80)

        if self.print_cmd:
            print(f'[CMD]: {cmd}')

        p = Popen(args=shlex.split(cmd), shell=self.shell)
        p.wait()

        if self.print_cmd:
            print('=' * 80)

        if self.exit_non_zero and p.returncode != 0:
            print(
                f'Last command exited with non zero exit code. [{p.returncode}]')
            exit(1)

        return p.returncode

    def set_exit_non_zero(self, val: bool) -> None:
        self.exit_non_zero = val
