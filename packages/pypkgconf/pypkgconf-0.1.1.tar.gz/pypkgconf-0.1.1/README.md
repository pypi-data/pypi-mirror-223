This project provides Python bindings to [pkgconf](http://pkgconf.org/).

## Building `pypkgconf` wheel

```
pip install build
python -m build
```

### Building on Windows

On Windows, you want to link with the `static` version of libpkgconf.
You also want to use `release` buildtype.

```
pip install build
python -m build  -Csetup-args="-Ddefault_library=static" -Csetup-args="-Dbuildtype=release"
```


## Running tests

You need a recent version of `meson`.

```
pip install pytest cffi
meson setup . build
meson test -C build
```


## Using pypkgconf

The API is very close to the original C code.

### cli-like API

This high-level API uses same arguments as the `pkgconf` executable.

Results are returned as a list of string (the list may be empty).
Errors and warnings are logger using the standard Python logging module, under
the `pkgconf` logger.
In case or error result, a `pypkgconf.PkgConfError` exception is raised.

#### `pypkgconf.query_args(command: str, env: dict[str, str] | None = None) -> list[str]`

The command is just like the command line arguments (e.g.: `"--libs foo"`)

If `env` is provided, pkgconf will use it for any envvar it queries.
If `env` is `None` (default), `os.environ` is used.

#### `pypkgconf.query(args: list[str] | None, **kwargs) -> list[str]`

Positional arguments are given as a list of strings.

Optional arguments are given either using an union of `pypkgconf.Flags`,
or as keyword arguments, depending if it is a boolean value or not.


### low-level API

The cffi interface to c function is provided through
`pypkgconf._libpkgconf.lib` and `pypkgconf._libpkgconf.ffi`.

Please refer to [pkgconf](https://github.com/pkgconf/pkgconf) code and
to [cffi](https://cffi.readthedocs.io/en/latest/ref.html) documentation,
or use the high-level interface as a reference on how to use it.
