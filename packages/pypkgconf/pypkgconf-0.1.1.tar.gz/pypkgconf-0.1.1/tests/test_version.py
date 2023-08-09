import pypkgconf

import pytest


def test_atleast(lib1_env):
    assert pypkgconf.query_args("--atleast-version 1.0 foo", env=lib1_env) == []

    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args("--atleast-version 2.0 foo", env=lib1_env)


def test_exact(lib1_env):
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args("--exact-version 1.0 foo", env=lib1_env)

    assert pypkgconf.query_args("--exact-version 1.2.3 foo", env=lib1_env) == []


def test_max(lib1_env):
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args("--max-version 1.0 foo", env=lib1_env)

    assert pypkgconf.query_args("--max-version 2.0 foo", env=lib1_env) == []
