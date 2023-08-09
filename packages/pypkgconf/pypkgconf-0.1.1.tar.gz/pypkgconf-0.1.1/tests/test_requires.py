import pypkgconf

import pytest

import sys


skip_pure = pytest.mark.skipif(
    sys.platform in {"win32", "cygwin", "msys"},
    reason="default personality is pure on Windows",
)


def test_libs(lib1_env):
    result = pypkgconf.query_args("--libs bar", env=lib1_env)
    assert result == ["-L/test/lib", "-lbar", "-lfoo"]


def test_cflags(lib1_env):
    result = pypkgconf.query_args("--libs --cflags baz", env=lib1_env)
    assert result == ["-fPIC", "-I/test/include/foo", "-L/test/lib", "-lbaz"]


@skip_pure
def test_libs_static(lib1_env):
    result = pypkgconf.query_args("--static --libs baz", env=lib1_env)
    assert result == [
        "-L/test/lib",
        "-lbaz",
        "-L/test/lib",
        "-lzee",
        "-L/test/lib",
        "-lfoo",
    ]


def test_libs_static_pure(lib1_env):
    result = pypkgconf.query_args("--static --pure --libs baz", env=lib1_env)
    assert result == ["-L/test/lib", "-lbaz", "-L/test/lib", "-lfoo"]


def test_argv_parse2(lib1_env):
    result = pypkgconf.query_args("--static --libs argv-parse-2", env=lib1_env)
    assert result == ["-llib-1", "-pthread", "/test/lib/lib2.so"]


@skip_pure
def test_static_cflags(lib1_env):
    result = pypkgconf.query_args("--static --cflags baz", env=lib1_env)
    assert result == ["-fPIC", "-I/test/include/foo", "-DFOO_STATIC"]


@skip_pure
def test_private_duplication(lib1_env):
    result = pypkgconf.query_args(
        "--static --libs-only-l private-libs-duplication", env=lib1_env
    )
    assert result == ["-lprivate", "-lbaz", "-lzee", "-lbar", "-lfoo", "-lfoo"]


@skip_pure
def test_libs_static2(lib1_env):
    result = pypkgconf.query_args("--static --libs static-libs", env=lib1_env)
    assert result == ["-lbar", "-lbar-private", "-L/test/lib", "-lfoo"]


def test_missing(lib1_env):
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args("--cflags missing-require", env=lib1_env)


@skip_pure
def test_requires_internal(testsdir):
    selfdir = testsdir.as_posix()

    result = pypkgconf.query_args(
        f'--with-path="{selfdir}/lib1" --static --libs requires-internal'
    )
    assert result == ["-lbar", "-lbar-private", "-L/test/lib", "-lfoo"]


def test_requires_internal_missing(testsdir):
    selfdir = testsdir.as_posix()

    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args(
            f'--with-path="{selfdir}/lib1" --static --libs requires-internal-missing'
        )


def test_requires_internal_collision(testsdir):
    selfdir = testsdir.as_posix()

    result = pypkgconf.query_args(
        f'--with-path="{selfdir}/lib1" --cflags requires-internal-collision'
    )
    assert result == ["-I/test/local/include/foo"]


def test_orphaned_requires_private(testsdir):
    selfdir = testsdir.as_posix()

    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args(
            f'--with-path="{selfdir}/lib1" --cflags --libs orphaned-requires-private'
        )
