# helper funcs
from pathlib import Path


def mkdir(path: str) -> None:
    Path(path).mkdir(exist_ok=True, parents=True)


def touch(filepath: str) -> None:
    Path(filepath).touch()


create_file = touch
