# BuildMe 🛠️

Another build system. A simple command runner thats it.

# What is BuildMe 🤔️

Well this pretty much sums it up.

![xkcd comic](https://imgs.xkcd.com/comics/standards.png)

# Why???

IDK. I saw this comic and decided that I want a build system of my own.

And,

- Makefile's are shit.
- Cmake is complicated
- Meson requires two dependencies (Meson and Ninja)
- Bazel, corporate BS

It does come with some feature.

- It is just command runner (Does not give an _f_ about the file or it's mod time)
- It's just python. Anything that works on python works on buildme script.
  - you want a build script that has access to `pandas`, well you can now have it.

# Docs 🧾️

- Install buildme

```console
pip3 install git+https://github.com/Adwaith-Rajesh/buildme.git
OR
pip3 install buildme
```

- Create a `buildme` script
  > The shebang is IMPORTANT (This thingy -> #!/bin/env buildme)

```python
#!/bin/env buildme
from argparse import Namespace  # for type hinting purposes only
from buildme import CommandRunner, target


cr = CommandRunner(
    shell=False,  # prevents invoking 'mystery' programs (default=False)
    print_cmd=True,  # prints the command that is currently being executed (default=True)
    print_cmd_sep=True,  # prints a separation line between the commands that are ran (default=True)
    exit_non_zero=True,  # exit the buildme execution if a command exits non zero (default=True)
)

# you can override the exit_no_zero using the
# method CommandRunner.set_exit_non_zero(vel: bool)


@target(depends=['test'])
def hello(opts: Namespace, _):
    print(opts)
    code = cr.run('echo Hello World')
    print(f'{code=}')


@target()
def test(opts: Namespace, _):
    if getattr(opts, 'release', None) is not None and opts.release == '0':
        print('release is zero')
    print('This from test')


@target()
def foo(_, __):
    print('This is the foo target')


@target()
def bar(_, __):
    print('This is the bar target')


@target(depends=['test'])
def all(_, __): pass

```

- Make it executable

```console
chmod +x ./buildme
```

- Have Fun

```console
$ ./buildme hello
This from test
Namespace()
================================================================================
[CMD]: echo Hello World
Hello World
================================================================================
code=0
```

> Order matters

```console
$ ./buildme foo bar
This is the foo target
This is the bar target

$ ./buildme bar foo
This is the bar target
This is the foo target

```

- Helper functions

`buildme` has currently two helper functions

```python
from buildme import mkdir, touch, rmdir, rm, get_files_in_dir
```

# Bye....
