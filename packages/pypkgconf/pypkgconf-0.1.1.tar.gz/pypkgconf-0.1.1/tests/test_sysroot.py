import pypkgconf


def test_do_not_eat_slash(lib1_env):
    env = {"PKG_CONFIG_SYSROOT_DIR": "/"}
    env.update(lib1_env)

    result = pypkgconf.query_args("--cflags baz", env=env)
    assert result == ["-fPIC", "-I/test/include/foo"]


def test_cflags(testsdir, lib1_env):
    selfdir = testsdir.as_posix()
    env = {"PKG_CONFIG_SYSROOT_DIR": selfdir}
    env.update(lib1_env)

    result = pypkgconf.query_args("--cflags baz", env=env)
    assert result == ["-fPIC", f"-I{selfdir}/test/include/foo"]


def test_variable(testsdir, lib1_env):
    selfdir = testsdir.as_posix()
    env = {"PKG_CONFIG_SYSROOT_DIR": selfdir}
    env.update(lib1_env)

    result = pypkgconf.query_args("--variable=prefix foo", env=env)
    assert result == [f"{selfdir}/test"]

    result = pypkgconf.query_args("--variable=includedir foo", env=env)
    assert result == [f"{selfdir}/test/include"]


def test_do_not_duplicate_sysroot_dir(testsdir, lib1_env):
    env = {"PKG_CONFIG_SYSROOT_DIR": "/sysroot"}
    env.update(lib1_env)

    result = pypkgconf.query_args("--cflags sysroot-dir-2", env=env)
    assert result == ["-I/sysroot/usr/include"]

    result = pypkgconf.query_args("--cflags sysroot-dir-3", env=env)
    assert result == ["-I/sysroot/usr/include"]

    result = pypkgconf.query_args("--cflags sysroot-dir-5", env=env)
    assert result == ["-I/sysroot/usr/include"]

    selfdir = testsdir.as_posix()
    env["PKG_CONFIG_SYSROOT_DIR"] = selfdir
    result = pypkgconf.query_args("--cflags sysroot-dir-4", env=env)
    assert result == [f"-I{selfdir}/usr/include"]


def test_uninstalled(lib1_env):
    env = {"PKG_CONFIG_SYSROOT_DIR": "/sysroot"}
    env.update(lib1_env)

    result = pypkgconf.query_args("--libs omg", env=env)
    assert result == ["-L/test/lib", "-lomg"]


def test_uninstalled_pkgconf1(lib1_env):
    env = {
        "PKG_CONFIG_SYSROOT_DIR": "/sysroot",
        "PKG_CONFIG_PKGCONF1_SYSROOT_RULES": "1",
    }
    env.update(lib1_env)

    result = pypkgconf.query_args("--libs omg", env=env)
    assert result == ["-L/sysroot/test/lib", "-lomg"]


def test_uninstalled_fdo(lib1_env):
    env = {
        "PKG_CONFIG_SYSROOT_DIR": "/sysroot",
        "PKG_CONFIG_FDO_SYSROOT_RULES": "1",
    }
    env.update(lib1_env)

    result = pypkgconf.query_args("--libs omg", env=env)
    assert result == ["-L/test/lib", "-lomg"]


def test_uninstalled_fdo_pc_sysrootdir(lib1_env):
    env = {
        "PKG_CONFIG_SYSROOT_DIR": "/sysroot",
        "PKG_CONFIG_FDO_SYSROOT_RULES": "1",
    }
    env.update(lib1_env)

    result = pypkgconf.query_args("--libs omg-sysroot", env=env)
    assert result == ["-L/sysroot/test/lib", "-lomg"]
