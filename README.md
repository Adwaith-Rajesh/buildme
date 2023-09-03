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
  - v0.3.0 onwards, buildme does give an _f_ about the file and it's mod times (times have changed)
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
from buildme import CommandRunner, target

cr = CommandRunner()

@target()
def foo(_, __):
    print('This is the foo target')


@target()
def bar(_, __):
    cr.run('echo this is from bar target')


@target(depends=['foo', 'bar'])
def all(_, __): pass

```

- Make it executable

```console
$ ./buildme foo
This is the foo target

$ ./buildme bar
================================================================================
[CMD]: echo this is from bar target
this is from bar target
================================================================================

$ ./buildme all
This is the foo target
================================================================================
[CMD]: echo this is from bar target
this is from bar target
================================================================================
```

# Bye....
