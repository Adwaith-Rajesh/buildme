import argparse


def _get_buildme_file_contents(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def _create_build_script_code(old_code: str, targets: list[str], usr_opt_var_name: str) -> str:
    return old_code + ''.join(f'\n{t}({usr_opt_var_name})' for t in targets)


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
    usr_known_args_var_name = f'{usr_known_args=}'.split(
        '=')[0]  # gets the var name as string

    new_buildme_code = _create_build_script_code(
        _get_buildme_file_contents(args.path),
        args.targets,
        usr_known_args_var_name
    )

    # the dangerous part
    exec(new_buildme_code, {
         usr_known_args_var_name: usr_known_args, **globals()})

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
