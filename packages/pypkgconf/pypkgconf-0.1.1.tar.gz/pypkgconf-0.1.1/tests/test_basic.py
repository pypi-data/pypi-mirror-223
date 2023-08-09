import pypkgconf

import pytest

import shutil


def test_noargs(lib1_env):
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args("", env=lib1_env)


def test_libs(lib1_env):
    result = pypkgconf.query_args("--libs foo", env=lib1_env)

    assert result == ["-L/test/lib", "-lfoo"]


def test_libs_cflags(lib1_env):
    result = pypkgconf.query_args("--cflags --libs foo", env=lib1_env)

    assert result == ["-fPIC", "-I/test/include/foo", "-L/test/lib", "-lfoo"]


def test_libs_cflags_version(lib1_env):
    result = pypkgconf.query_args('--cflags --libs "foo > 1.2"', env=lib1_env)

    assert result == ["-fPIC", "-I/test/include/foo", "-L/test/lib", "-lfoo"]


def test_libs_cflags_version_multiple(lib1_env):
    result = pypkgconf.query_args(
        '--cflags --libs "foo > 1.2 bar >= 1.3"', env=lib1_env
    )

    assert result == ["-fPIC", "-I/test/include/foo", "-L/test/lib", "-lbar", "-lfoo"]


def test_libs_cflags_version_multiple_coma(lib1_env):
    result = pypkgconf.query_args(
        '--cflags --libs "foo > 1.2,bar >= 1.3"', env=lib1_env
    )

    assert result == ["-fPIC", "-I/test/include/foo", "-L/test/lib", "-lbar", "-lfoo"]


def test_libs_cflags_version_alt(lib1_env):
    result = pypkgconf.query_args('--cflags --libs "foo" ">" "1.2"', env=lib1_env)

    assert result == ["-fPIC", "-I/test/include/foo", "-L/test/lib", "-lfoo"]


def test_libs_cflags_version_different(lib1_env):
    result = pypkgconf.query_args('--cflags --libs "foo" "!=" "1.3.0"', env=lib1_env)

    assert result == ["-fPIC", "-I/test/include/foo", "-L/test/lib", "-lfoo"]


def test_libs_cflags_version_different_bad(caplog, lib1_env):
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--cflags --libs "foo" "!=" "1.2.3"', env=lib1_env)

    assert (
        "Package dependency requirement 'foo != 1.2.3' could not be satisfied.\n"
        in caplog.text
    )
    assert (
        "Package 'foo' has version '1.2.3', required version is '!= 1.2.3'\n"
        in caplog.text
    )


def test_exists_nonexitent(lib1_env):
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args("--exists nonexistant", env=lib1_env)


def test_nonexitent(lib1_env):
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args("nonexistant", env=lib1_env)


def test_exists_version(lib1_env):
    assert pypkgconf.query_args('--exists "foo > 1.2"', env=lib1_env) == []


def test_exists_version_bad(lib1_env):
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--exists "foo > 1.2.3"', env=lib1_env)


def test_exists_version_bad(lib1_env):
    assert pypkgconf.query_args('--exists "foo" ">" "1.2"', env=lib1_env) == []


def test_uninstalled_bad(lib1_env):
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--uninstalled "foo"', env=lib1_env)


def test_uninstalled(lib1_env):
    assert pypkgconf.query_args('--uninstalled "omg"', env=lib1_env) == []


def test_exists_version_bad2(lib1_env):
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--exists "foo >= "', env=lib1_env)


def test_exists_version_bad3(lib1_env):
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--exists "tilde >= 1.0.0"', env=lib1_env)


def test_exists(lib1_env):
    assert pypkgconf.query_args('--exists "tilde = 1.0.0~rc1"', env=lib1_env) == []


def test_exists2(lib1_env):
    assert pypkgconf.query_args('--exists "tilde <= 1.0.0"', env=lib1_env) == []


def test_exists3(lib1_env):
    assert pypkgconf.query_args('--exists "" "foo"', env=lib1_env) == []


def test_libs_intermediary(lib1_env):
    result = pypkgconf.query_args("--libs intermediary-1 intermediary-2", env=lib1_env)

    assert result == ["-lintermediary-1", "-lintermediary-2", "-lfoo", "-lbar", "-lbaz"]


def test_libs_circular2(caplog, lib1_env):
    assert pypkgconf.query_args("circular-2 --validate", env=lib1_env) == []
    assert (
        "circular-1: breaking circular reference (circular-1 -> circular-2 -> circular-1)\n"
        in caplog.text
    )


def test_libs_circular1(caplog, lib1_env):
    assert pypkgconf.query_args("circular-1 --validate", env=lib1_env) == []
    assert (
        "circular-3: breaking circular reference (circular-3 -> circular-1 -> circular-3)\n"
        in caplog.text
    )


def test_libs_circular_directpc(testsdir, lib1_env):
    result = pypkgconf.query_args(
        f"--libs {testsdir.as_posix()}/lib1/circular-3.pc", env=lib1_env
    )

    assert result == ["-lcircular-2", "-lcircular-3", "-lcircular-1"]


def test_libs_static(lib1_env):
    result = pypkgconf.query_args("--libs static-archive-libs", env=lib1_env)

    assert result == ["/libfoo.a", "-pthread"]


def test_libs_static_ordering(lib1_env):
    result = pypkgconf.query_args("--libs foo bar", env=lib1_env)

    assert result == ["-L/test/lib", "-lbar", "-lfoo"]


def test_pkg_config_path(lib1_lib2_env):
    result = pypkgconf.query_args("--libs foo", env=lib1_lib2_env)

    assert result == ["-L/test/lib", "-lfoo"]

    result = pypkgconf.query_args("--libs bar", env=lib1_lib2_env)

    assert result == ["-L/test/lib", "-lbar", "-lfoo"]


def test_with_path(testsdir):
    lib1_path = testsdir / "lib1"
    lib2_path = testsdir / "lib2"

    result = pypkgconf.query_args(
        f"--with-path={lib1_path.as_posix()} --with-path={lib2_path.as_posix()} --libs foo"
    )

    assert result == ["-L/test/lib", "-lfoo"]

    result = pypkgconf.query_args(
        f"--with-path={lib1_path.as_posix()} --with-path={lib2_path.as_posix()} --libs bar"
    )

    assert result == ["-L/test/lib", "-lbar", "-lfoo"]


def test_nolibs(lib1_env):
    assert pypkgconf.query_args("--libs nolib", env=lib1_env) == []


def test_nocflags(lib1_env):
    assert pypkgconf.query_args("--cflags nocflag", env=lib1_env) == []


def test_arbitary_path(testsdir, tmp_path, monkeypatch):
    shutil.copy(testsdir / "lib1" / "foo.pc", tmp_path)
    monkeypatch.chdir(tmp_path)

    result = pypkgconf.query_args("--libs foo.pc")

    assert result == ["-L/test/lib", "-lfoo"]


def test_relocatable(testsdir):
    basedir = pypkgconf.query_args(f"--relocate {testsdir.as_posix()}")[0]

    result = pypkgconf.query_args(
        f"--define-prefix --variable=prefix {basedir}/lib-relocatable/lib/pkgconfig/foo.pc"
    )

    assert result == [f"{basedir}/lib-relocatable"]


def test_single_depth_selectors(testsdir):
    env = {"PKG_CONFIG_MAXIMUM_TRAVERSE_DEPTH": "1"}

    result = pypkgconf.query_args(
        f"--with-path={testsdir.as_posix()}/lib3 --print-requires bar", env=env
    )

    assert result == ["foo"]


def test_license_isc(testsdir):
    result = pypkgconf.query_args(
        f"--with-path={testsdir.as_posix()}/lib1 --license foo"
    )

    assert result == ["foo: ISC"]


def test_license_noassertion(testsdir):
    result = pypkgconf.query_args(
        f"--with-path={testsdir.as_posix()}/lib1 --license bar"
    )

    assert result == ["bar: NOASSERTION", "foo: ISC"]


def test_modversion_noflatten(testsdir):
    result = pypkgconf.query_args(
        f"--with-path={testsdir.as_posix()}/lib1 --modversion bar"
    )

    assert result == ["1.3"]
