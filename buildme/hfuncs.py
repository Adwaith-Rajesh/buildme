# helper funcs
import glob
import shutil
import sys
import warnings
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
    if sys.version_info.major == 3 and sys.version_info.minor > 10:
        return glob.glob(dir_pattern, recursive=recurse, include_hidden=include_hidden)
    if sys.version_info.major == 3 and sys.version_info.minor <= 10:
        if recurse is True:
            warnings.warn('recurs=True is not implemented for Python 3.10',
                          UserWarning, stacklevel=2)
        return glob.glob(dir_pattern, recursive=recurse)
    return []


def get_file_name(path: str) -> str:
    """gets file name from its path"""
    return Path(path).name


create_file = touch
