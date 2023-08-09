import pypkgconf


def test_libs(lib1_env):
    result = pypkgconf.query_args('--libs conflicts', env=lib1_env)

    assert result == ['-L/test/lib', '-lconflicts']


def test_ignore(lib1_env):
    result = pypkgconf.query_args('--ignore-conflicts --libs conflicts', env=lib1_env)

    assert result == ['-L/test/lib', '-lconflicts']
