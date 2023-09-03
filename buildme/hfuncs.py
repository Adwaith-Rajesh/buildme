# helper funcs
import glob
import shutil
from pathlib import Path


def mkdir(path: str) -> None:
    Path(path).mkdir(exist_ok=True, parents=True)


def touch(filepath: str) -> None:
    Path(filepath).touch()


def rmdir(path: str) -> None:
    if Path(path).is_dir():
        shutil.rmtree(path)


def rm(path: str) -> None:
    Path(path).unlink(missing_ok=True)


def get_files_in_dir(dir_pattern: str, recurse: bool = False,
                     include_hidden: bool = False) -> list[str]:
    return glob.glob(dir_pattern, recursive=recurse, include_hidden=include_hidden)


def get_file_name(path: str) -> str:
    """gets file name from its path"""
    return Path(path).name


create_file = touch
