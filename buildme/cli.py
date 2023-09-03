import argparse
import sys
from itertools import compress
from typing import Any

from buildme.core import _check_target_exists
from buildme.core import _exec_target


def _get_buildme_file_contents(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def _check_target_exists_map(targets: list[str]) -> list[bool]:
    return [_check_target_exists(name) for name in targets]


def main() -> int:
    parser = argparse.ArgumentParser()
    user_arg_parser = argparse.ArgumentParser()

    parser.add_argument('path', type=str, help='path to the buildme script')
    parser.add_argument('targets', type=str, nargs='*',
                        help='The list of targets to run')

    args, unknown = parser.parse_known_args()

    for a in unknown:
        if a.startswith(('-', '--')):
            user_arg_parser.add_argument(a.split('=')[0], type=str)

    usr_known_args, _ = user_arg_parser.parse_known_args()

    target_globals: dict[str, Any] = {}
    exec(_get_buildme_file_contents(args.path), target_globals)

    if not all(invalid_map := _check_target_exists_map(targets=args.targets)):
        print('unknown target(s): ' + ' '.join(compress(args.targets, [not i for i in invalid_map])),
              file=sys.stderr)
        return 1

    for t in args.targets:
        _exec_target(t, usr_known_args, target_globals)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
