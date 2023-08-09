import pypkgconf

import pytest


def test_simple(lib1_env):
    result = pypkgconf.query_args("--print-provides provides", env=lib1_env)
    assert result == [
        "provides-test-foo = 1.0.0",
        "provides-test-bar > 1.1.0",
        "provides-test-baz >= 1.1.0",
        "provides-test-quux < 1.2.0",
        "provides-test-moo <= 1.2.0",
        "provides-test-meow != 1.3.0",
        "provides = 1.2.3",
    ]

    result = pypkgconf.query_args("--libs provides-request-simple", env=lib1_env)
    assert result == ["-lfoo"]

    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args(
            "--no-provides --libs provides-request-simple", env=lib1_env
        )


def test_foo(lib1_env):
    assert pypkgconf.query_args("--libs provides-test-foo", env=lib1_env) == ["-lfoo"]
    assert pypkgconf.query_args('--libs "provides-test-foo = 1.0.0"', env=lib1_env) == [
        "-lfoo"
    ]
    assert pypkgconf.query_args(
        '--libs "provides-test-foo >= 1.0.0"', env=lib1_env
    ) == ["-lfoo"]
    assert pypkgconf.query_args(
        '--libs "provides-test-foo <= 1.0.0"', env=lib1_env
    ) == ["-lfoo"]
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--libs "provides-test-foo != 1.0.0"', env=lib1_env)
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--libs "provides-test-foo > 1.0.0"', env=lib1_env)
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--libs "provides-test-foo < 1.0.0"', env=lib1_env)


def test_bar(lib1_env):
    assert pypkgconf.query_args("--libs provides-test-bar", env=lib1_env) == ["-lfoo"]
    assert pypkgconf.query_args('--libs "provides-test-bar = 1.1.1"', env=lib1_env) == [
        "-lfoo"
    ]
    assert pypkgconf.query_args(
        '--libs "provides-test-bar >= 1.1.1"', env=lib1_env
    ) == ["-lfoo"]
    assert pypkgconf.query_args(
        '--libs "provides-test-bar <= 1.1.1"', env=lib1_env
    ) == ["-lfoo"]
    assert pypkgconf.query_args(
        '--libs "provides-test-bar != 1.1.0"', env=lib1_env
    ) == ["-lfoo"]
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--libs "provides-test-bar != 1.1.1"', env=lib1_env)
    assert pypkgconf.query_args('--libs "provides-test-bar > 1.1.1"', env=lib1_env) == [
        "-lfoo"
    ]
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--libs "provides-test-bar <= 1.1.0"', env=lib1_env)
    assert pypkgconf.query_args(
        '--libs "provides-test-bar <= 1.2.0"', env=lib1_env
    ) == ["-lfoo"]


def test_bar(lib1_env):
    assert pypkgconf.query_args("--libs provides-test-baz", env=lib1_env) == ["-lfoo"]
    assert pypkgconf.query_args('--libs "provides-test-baz = 1.1.0"', env=lib1_env) == [
        "-lfoo"
    ]
    assert pypkgconf.query_args(
        '--libs "provides-test-baz >= 1.1.0"', env=lib1_env
    ) == ["-lfoo"]
    assert pypkgconf.query_args(
        '--libs "provides-test-baz <= 1.1.0"', env=lib1_env
    ) == ["-lfoo"]
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--libs "provides-test-baz != 1.1.0"', env=lib1_env)
    assert pypkgconf.query_args(
        '--libs "provides-test-baz !- 1.0.0"', env=lib1_env
    ) == ["-lfoo"]
    assert pypkgconf.query_args('--libs "provides-test-baz > 1.1.1"', env=lib1_env) == [
        "-lfoo"
    ]
    assert pypkgconf.query_args('--libs "provides-test-baz > 1.1.0"', env=lib1_env) == [
        "-lfoo"
    ]
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--libs "provides-test-baz < 1.1.0"', env=lib1_env)
    assert pypkgconf.query_args('--libs "provides-test-baz < 1.2.0"', env=lib1_env) == [
        "-lfoo"
    ]


def test_quux(lib1_env):
    assert pypkgconf.query_args("--libs provides-test-quux", env=lib1_env) == ["-lfoo"]
    assert pypkgconf.query_args(
        '--libs "provides-test-quux = 1.1.9"', env=lib1_env
    ) == ["-lfoo"]
    assert pypkgconf.query_args(
        '--libs "provides-test-quux >= 1.1.0"', env=lib1_env
    ) == ["-lfoo"]
    assert pypkgconf.query_args(
        '--libs "provides-test-quux >= 1.1.9"', env=lib1_env
    ) == ["-lfoo"]
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--libs "provides-test-quux >= 1.2.0"', env=lib1_env)
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--libs "provides-test-quux <= 1.2.0"', env=lib1_env)
    assert pypkgconf.query_args(
        '--libs "provides-test-quux <= 1.1.9"', env=lib1_env
    ) == ["-lfoo"]
    assert pypkgconf.query_args(
        '--libs "provides-test-quux != 1.2.0"', env=lib1_env
    ) == ["-lfoo"]
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--libs "provides-test-quux != 1.1.0"', env=lib1_env)
    assert pypkgconf.query_args(
        '--libs "provides-test-quux > 1.1.9"', env=lib1_env
    ) == ["-lfoo"]
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--libs "provides-test-quux > 1.2.0"', env=lib1_env)
    assert pypkgconf.query_args(
        '--libs "provides-test-quux < 1.1.0"', env=lib1_env
    ) == ["-lfoo"]
    # FIXME: Test duplicated...
    # with pytest.raises(pypkgconf.PkgConfError):
    #     pypkgconf.query_args('--libs "provides-test-quux > 1.2.0"')


def test_moo(lib1_env):
    assert pypkgconf.query_args("--libs provides-test-moo", env=lib1_env) == ["-lfoo"]
    assert pypkgconf.query_args('--libs "provides-test-moo = 1.2.0"', env=lib1_env) == [
        "-lfoo"
    ]
    assert pypkgconf.query_args(
        '--libs "provides-test-moo >= 1.1.0"', env=lib1_env
    ) == ["-lfoo"]
    assert pypkgconf.query_args(
        '--libs "provides-test-moo >= 1.2.0"', env=lib1_env
    ) == ["-lfoo"]
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--libs "provides-test-moo >= 1.2.1"', env=lib1_env)
    assert pypkgconf.query_args(
        '--libs "provides-test-moo <= 1.2.0"', env=lib1_env
    ) == ["-lfoo"]
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--libs "provides-test-moo != 1.1.0"', env=lib1_env)
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--libs "provides-test-moo != 1.0.0"', env=lib1_env)
    assert pypkgconf.query_args('--libs "provides-test-moo > 1.1.9"', env=lib1_env) == [
        "-lfoo"
    ]
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--libs "provides-test-moo > 1.2.0"', env=lib1_env)
    assert pypkgconf.query_args('--libs "provides-test-moo < 1.1.0"', env=lib1_env) == [
        "-lfoo"
    ]
    assert pypkgconf.query_args('--libs "provides-test-moo < 1.2.0"', env=lib1_env) == [
        "-lfoo"
    ]


def test_meow(lib1_env):
    assert pypkgconf.query_args("--libs provides-test-meow", env=lib1_env) == ["-lfoo"]
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--libs "provides-test-meow = 1.3.0"', env=lib1_env)
    assert pypkgconf.query_args(
        '--libs "provides-test-meow != 1.3.0"', env=lib1_env
    ) == ["-lfoo"]
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--libs "provides-test-meow > 1.2.0"', env=lib1_env)
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--libs "provides-test-meow < 1.3.1"', env=lib1_env)
    assert pypkgconf.query_args(
        '--libs "provides-test-meow < 1.3.0"', env=lib1_env
    ) == ["-lfoo"]
    assert pypkgconf.query_args(
        '--libs "provides-test-meow > 1.3.0"', env=lib1_env
    ) == ["-lfoo"]
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--libs "provides-test-meow >= 1.3.0"', env=lib1_env)
    assert pypkgconf.query_args(
        '--libs "provides-test-meow >= 1.3.1"', env=lib1_env
    ) == ["-lfoo"]
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--libs "provides-test-meow <= 1.3.0"', env=lib1_env)
    assert pypkgconf.query_args(
        '--libs "provides-test-meow < 1.2.0"', env=lib1_env
    ) == ["-lfoo"]


def test_indirect_dependency_node(testsdir):
    selfdir = (testsdir / "lib1").as_posix()

    result = pypkgconf.query_args(
        f'--with-path="{selfdir}" --modversion "provides-test-meow"'
    )
    assert result == ["1.2.3"]

    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args(
            f'--with-path="{selfdir}" --modversion "provides-test-meow = 1.3.0"'
        )
