from pypkgconf import pkgconf_version, pypkgconf_version, query, Flags

import pytest


try:
    from importlib.metadata import version

    package_version = version('pypkgconf')

except Exception:
    package_version = None


@pytest.mark.skipif(package_version is None, reason="Python too old or package not installed")
def test_pypkgconf_version():
    assert pypkgconf_version() == package_version


def test_pkgconf_version():
    version = query(want_flags=Flags.VERSION)
    assert pkgconf_version() == version[0]
