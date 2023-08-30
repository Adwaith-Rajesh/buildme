import shlex
import sys
from subprocess import PIPE
from subprocess import Popen


class CommandRunner:
    def __init__(self, shell: bool = False, print_cmd: bool = True) -> None:
        self.shell = shell
        self.print_cmd = print_cmd

    def run(self, cmd: str) -> None:
        if self.print_cmd:
            print(f'[CMD]: {cmd}')

        with Popen(args=shlex.split(cmd), shell=self.shell, stdout=PIPE) as p:
            if p.stdout:
                sys.stdout.write(p.stdout.read().decode('utf-8'))
