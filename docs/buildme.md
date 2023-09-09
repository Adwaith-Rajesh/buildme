# Buildme scripts

You can name the script file whatever you want, but make sure to add the shebang
at the top of the file

```
#!/bin/env buildme
```

Then make the script script executable

```console
chmod +x ./script-name
```

For convenience, the script name in the docs will be '`buildme`'

# Target

A target is a python function that can be called from the CLI.

A target will run when invoked if:

- The target does not create any file (`@target(creates=[])`).
- The target does not depend on any files (`@target(depends=[])`).
- One of the files mentioned in `creates` does not exist.
- max mtimes (creates) < min mtimes (depends) (basically, if one of the files in `depends` updates).
  - kind of how makefile work.

---

### Creating a target

A target can be crated by decorating a function with `@target()`

```python
#!/bin/env buildme
from buildme import target

@target()  # same as @target(creates=[], depends=[])
def foo(_, __):  # the arguments that a target receives will be discussed below
    print('This is the foo target')
```

```console
$ ./buildme foo
This is the foo target
```

---

### Target depending on another target

```python
#!/bin/env buildme
from buildme import target

@target(depends=['bar'])
def foo(_, __):
    print('This is the foo target')


@target()
def bar(_, __):
    print('This is the bar target')
```

In the above example the target `foo` depends on the target `bar`. Thus when `foo` is invoked
the`bar` target run first.

```console
$ ./buildme foo
This is the bar target
This is the foo target
```

- #### order matters

```python
#!/bin/env buildme
from buildme import target


@target(depends=['bar', 'zoom'])
def foo(_, __):
    print('This is the foo target')


@target()
def bar(_, __):
    print('This is the bar target')


@target()
def zoom(_, __):
    print('This is the zoom target')
```

```console
$ ./buildme foo
This is the bar target
This is the zoom target
This is the foo target
```

```console
$ ./buildme zoom bar
This is the zoom target
This is the bar target
```

---

### Target depending on files

A target can also depends on the file/globs.

files/globs are mentioned using prefix '**f:**'

```python
#!/bin/env buildme
from buildme import target

@target(depends=['f:./*.c', 'f:./test.txt'])
def foo(_, __):
    print('This is the foo target')
```

Mentioning files as dependencies really does not make any sense until you mention
`creates` too, as it what determines whether the target runs or not when invoked.

---

### Targets that creates files

```python
#!/bin/env buildme
from buildme import CommandRunner, target

cr = CommandRunner()  # more on this below

@target(creates=['./hello'], depends=['f:hello.c'])
def hello(_, __):
    cr.run('gcc -o hello hello.c')
```

- Running for the first time

```console
$ ./buildme hello
================================================================================
[CMD]: gcc -o hello hello.c
================================================================================
```

- Running the command for the second time

```console
$ ./buildme hello
```

The target will not run as the source, or the files mentioned in `depends` did not change

---

### CommandRunner

The CommandRunner class loosely wraps the `subprocess.Popen` class. Making it easier to use.

```python
#!/bin/env buildme
from buildme import CommandRunner

cr = CommandRunner(
    shell=False,  # prevents invoking 'mystery' programs (default=False)
    print_cmd=True,  # prints the command that is currently being executed (default=True)
    print_cmd_sep=True,  # prints a separation line between the commands that are ran (default=True)
    exit_non_zero=True,  # exit the buildme execution if a command exits non zero (default=True)
)

cr.run('echo hello world')
```

```console
$ ./buildme
================================================================================
[CMD]: echo hello world
hello world
================================================================================
```

- `print_cmd_sep`

```python
#!/bin/env buildme
from buildme import CommandRunner

cr = CommandRunner(print_cmd_sep=False)
cr.run('echo hello world')
```

```console
$ ./buildme
[CMD]: echo hello world
hello world
```

- `print_cmd`

```python
#!/bin/env buildme
from buildme import CommandRunner

cr = CommandRunner(print_cmd=False)
cr.run('echo hello world')
```

```console
$ ./buildme
================================================================================
hello world
================================================================================
```

---

### Receiving Command line args

```python
#!/bin/env buildme
from buildme import target

@target()
def foo(opts, _):
    print(opts.name)
```

> The type of opts is `argparse.Namespace`

```console
$ ./buildme foo --name joe
joe
```

> make sure to check whether the argument exists before accessing it, as if, `--name` is not
> passed and `opts.name` is accessed this will lead to an `AttributeError`

```python
#!/bin/env buildme
from buildme import target

@target()
def foo(opts, _):
    if getattr(opts, 'name', None) is not None:
        print(opts.name)
```

---

### Getting info about the target itself

Let's you want to access the `creates` or `depends` or the `name` of the target itself, then
you can do the following

```python
#!/bin/env buildme
from buildme import target, CommandRunner

cr = CommandRunner()

@target(creates=['hello'], depends=['f:./hello.c'])
def hello(_, t_data):
    print(t_data.name)
    print(t_data.depends.files)
    print(t_data.depends.targets)
    print(t_data.creates.files)
    print(t_data.creates.func)  # more on this later

    cr.run('gcc -o hello hello.c')
```

```console
hello
['./hello.c']
[]
['hello']
None
================================================================================
[CMD]: gcc -o hello hello.c
================================================================================
```

---

### Dynamic 'creates'

Sometimes the name of files in 'creates' depends on the name of the files in 'depends', like
when object files are generated with same name as the c source file, just with different
extensions.

In such cases we can use dynamic 'creates'. Here you pass a function that can modify the
file names provided in depends

```python
#!/bin/env buildme
from buildme import target, get_file_name

# this does not effect the targets depends
@target(creates=lambda x: get_file_name(x).replace('.c', '.o'),
        depends=['f:./*.c']
)
def gen_o_files(_, t_data):
    print(t_data.depends.files)
    print(t_data.creates.files)

    ...
```

```console
$ ./buildme gen_o_files
['./hello.c']
['hello.o']
```

---

### The above two ides can combined to do this

```python

#!/bin/env buildme
from buildme import target, get_file_name, CommandRunner

cr = CommandRunner()

@target(creates=lambda x: get_file_name(x).replace('.c', ''),
        depends=['f:./*.c']
)
def hello(_, t_data):
    cr.run(f'gcc -o {t_data.creates.files[0]} {t_data.depends.files[0]}')
```

```console
$ ./buildme hello
================================================================================
[CMD]: gcc -o hello ./hello.c
================================================================================
```

---

### Helper functions

Buildme comes with a couple to helper function that makes creating, deleting files and
directories easy.

```python
#!/bin/env buildme

from buildme import mkdir, touch, rmdir, rm, get_file_name, get_files_in_dir

# mkdir -> creates a dir
# rmdir -> removes a dir
# touch -> creates a file
# rm    -> removes a file
# get_file_name -> get the filename from it's path
# fet_files_in_dir -> returns all the file that matches the path pattern
```

more info on these funcs can be found here: [hfuncs.py](/buildme/hfuncs.py)
