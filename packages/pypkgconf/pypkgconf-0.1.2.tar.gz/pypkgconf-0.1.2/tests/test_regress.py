import pypkgconf

import pytest

import logging
import os
import sys


def test_case_sensitivity(lib1_env):
    assert pypkgconf.query_args("--variable=foo case-sensitivity", env=lib1_env) == [
        "3"
    ]
    assert pypkgconf.query_args("--variable=Foo case-sensitivity", env=lib1_env) == [
        "4"
    ]


def test_depgraph_break_1(lib1_env):
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args(
            '--exists --print-errors "foo > 0.6.0 foo < 0.8.0"', env=lib1_env
        )


def test_depgraph_break_2(lib1_env):
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args(
            '--exists --print-errors "nonexisting foo <= 3"', env=lib1_env
        )


def test_depgraph_break_3(lib1_env):
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args('--exists --print-errors "depgraph-break"', env=lib1_env)


def test_define_variable(lib1_env):
    result = pypkgconf.query_args(
        '--variable=typelibdir --define-variable="libdir=\\${libdir}" typelibdir',
        env=lib1_env,
    )
    assert result == ["\\${libdir}/typelibdir"]


def test_define_variable_override(lib1_env):
    result = pypkgconf.query_args(
        '--variable=prefix --define-variable="prefix=/test" typelibdir', env=lib1_env
    )
    assert result == ["/test"]


def test_variable(lib1_env):
    result = pypkgconf.query_args("--variable=includedir foo", env=lib1_env)
    assert result == ["/test/include"]


def test_keep_system_libs(lib1_env):
    env = {"LIBRARY_PATH": "/test/local/lib"}
    env.update(lib1_env)

    assert pypkgconf.query_args("--libs-only-L cflags-libs-only", env=env) == []

    result = pypkgconf.query_args(
        "--libs-only-L --keep-system-libs cflags-libs-only", env=env
    )
    assert result == ["-L/test/local/lib"]


def test_libs(lib1_env):
    result = pypkgconf.query_args("--libs cflags-libs-only", env=lib1_env)
    assert result == ["-L/test/local/lib", "-lfoo"]


def test_libs_only(lib1_env):
    result = pypkgconf.query_args(
        "--libs-only-L --libs-only-l cflags-libs-only", env=lib1_env
    )
    assert result == ["-L/test/local/lib", "-lfoo"]


def test_libs_never_mergeback(lib1_env):
    result = pypkgconf.query_args("--libs prefix-foo1", env=lib1_env)
    assert result == ["-L/test/bar/lib", "-lfoo1"]

    result = pypkgconf.query_args("--libs prefix-foo1 prefix-foo2", env=lib1_env)
    assert result == ["-L/test/bar/lib", "-lfoo1", "-lfoo2"]


def test_cflags_only(lib1_env):
    result = pypkgconf.query_args(
        "--cflags-only-I --cflags-only-other cflags-libs-only", env=lib1_env
    )
    assert result == ["-I/test/local/include/foo"]


def test_cflags_never_mergeback(lib1_env):
    result = pypkgconf.query_args("--cflags prefix-foo1 prefix-foo2", env=lib1_env)
    assert result == ["-I/test/bar/include/foo", "-DBAR", "-fPIC", "-DFOO"]


def test_incomplete_libs(lib1_env):
    result = pypkgconf.query_args("--libs incomplete", env=lib1_env)
    assert result == []


def test_incomplete_cflags(lib1_env):
    result = pypkgconf.query_args("--cflags incomplete", env=lib1_env)
    assert result == []


def test_isystem_munge_order(lib1_env):
    result = pypkgconf.query_args("--cflags isystem", env=lib1_env)
    assert result == ["-isystem", "/opt/bad/include", "-isystem", "/opt/bad2/include"]


def test_isystem_munge_sysroot(testsdir, lib1_env):
    env = {"PKG_CONFIG_SYSROOT_DIR": testsdir.as_posix()}
    env.update(lib1_env)

    result = pypkgconf.query_args("--cflags isystem", env=env)

    assert f"-isystem {testsdir.as_posix()}/opt/bad/include" in " ".join(result)


def test_idirafter_munge_order(lib1_env):
    result = pypkgconf.query_args("--cflags idirafter", env=lib1_env)
    assert result == [
        "-idirafter",
        "/opt/bad/include",
        "-idirafter",
        "/opt/bad2/include",
    ]


def test_idirafter_munge_sysroot(testsdir, lib1_env):
    env = {"PKG_CONFIG_SYSROOT_DIR": testsdir.as_posix()}
    env.update(lib1_env)

    result = pypkgconf.query_args("--cflags idirafter", env=env)
    assert f"-idirafter {testsdir.as_posix()}/opt/bad/include" in " ".join(result)


def test_idirafter_ordering(lib1_env):
    result = pypkgconf.query_args("--cflags idirafter-ordering", env=lib1_env)
    assert result == [
        "-I/opt/bad/include1",
        "-idirafter",
        "-I/opt/bad/include2",
        "-I/opt/bad/include3",
    ]


def test_pcpath(testsdir, lib2_env):
    selfdir = testsdir.as_posix()

    result = pypkgconf.query_args(f"--cflags {selfdir}/lib3/bar.pc", env=lib2_env)
    assert result == ["-fPIC", "-I/test/include/foo"]


def test_sysroot_munge(tmp_path, testsdir):
    contents = (testsdir / "lib1" / "sysroot-dir.pc").read_text(encoding="utf-8")
    contents = contents.replace("/sysroot/", testsdir.as_posix() + "/")

    (tmp_path / "lib1").mkdir()
    (tmp_path / "lib1" / "sysroot-dir-selfdir.pc").write_text(
        contents, encoding="utf-8"
    )

    env = {
        "PKG_CONFIG_PATH": (tmp_path / "lib1").as_posix(),
        "PKG_CONFIG_SYSROOT_DIR": testsdir.as_posix(),
    }

    result = pypkgconf.query_args("--libs sysroot-dir-selfdir", env=env)
    assert result == [f"-L{testsdir.as_posix()}/lib", "-lfoo"]


def test_virtual_variable():
    assert pypkgconf.query_args("--exists pkg-config") == []
    assert pypkgconf.query_args("--exists pkgconf") == []

    if sys.platform in {"win32", "cygwin", "msys"}:
        pcpath = "../lib/pkgconfig;../share/pkgconfig"
    else:
        pcpath = os.environ.get("PKG_DEFAULT_PATH")
    result = pypkgconf.query_args("--variable=pc_path pkg-config")
    assert result == [pcpath]

    result = pypkgconf.query_args("--variable=pc_path pkgconf")
    assert result == [pcpath]


def test_fragment_collision(testsdir):
    selfdir = testsdir.as_posix()

    result = pypkgconf.query_args(
        f'--with-path="{selfdir}/lib1" --cflags fragment-collision'
    )
    assert result == ["-D_BAZ", "-D_BAR", "-D_FOO", "-D_THREAD_SAFE", "-pthread"]


def test_malformed_1(testsdir):
    selfdir = testsdir.as_posix()

    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args(f'--validate --with-path="{selfdir}/lib1" malformed-1')


def test_malformed_quoting(testsdir):
    selfdir = testsdir.as_posix()

    assert (
        pypkgconf.query_args(
            f'--validate --with-path="{selfdir}/lib1" malformed-quoting'
        )
        == []
    )


def test_explicit_sysroot(monkeypatch, testsdir):
    # FIXME: does not work with drive letter...
    selfdir = testsdir.as_posix().removeprefix(testsdir.drive)
    monkeypatch.setenv("PKG_CONFIG_SYSROOT_DIR", selfdir)

    result = pypkgconf.query_args(
        f'--debug --with-path="{selfdir}/lib1" --variable=pkgdatadir explicit-sysroot'
    )
    assert result == [f"{selfdir}/usr/share/test"]


def test_empty_tuple(testsdir):
    selfdir = testsdir.as_posix()

    assert (
        pypkgconf.query_args(f'--with-path="{selfdir}/lib1" --cflags empty-tuple') == []
    )


def test_solver_requires_private_debounce(testsdir):
    selfdir = testsdir.as_posix()

    result = pypkgconf.query_args(
        f'--with-path="{selfdir}/lib1" --cflags --libs metapackage'
    )
    assert result == [
        "-I/metapackage-1",
        "-I/metapackage-2",
        "-lmetapackage-1",
        "-lmetapackage-2",
    ]


def test_solver_requires_private_debounce(testsdir, caplog):
    selfdir = testsdir.as_posix()

    with caplog.at_level(logging.WARNING):
        assert (
            pypkgconf.query_args(
                f'--with-path="{selfdir}/lib1" --validate billion-laughs'
            )
            == []
        )

    s = 0
    for r in caplog.records:
        if (
            r.levelno == logging.WARNING
            and r.msg == "warning: truncating very long variable to 64KB"
        ):
            s += 1
    assert s == 5


def test_maximum_package_depth_off_by_one(testsdir):
    selfdir = testsdir.as_posix()

    result = pypkgconf.query_args(
        f'--with-path="{selfdir}/lib1" --modversion foo bar baz'
    )
    assert result == ["1.2.3"]
