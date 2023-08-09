import pypkgconf


def test_libs(lib1_env):
    result = pypkgconf.query_args('--libs framework-1', env=lib1_env)
    assert result == ['-F/test/lib', '-framework', 'framework-1']

    result = pypkgconf.query_args('--libs framework-2', env=lib1_env)
    assert result == ['-F/test/lib', '-framework', 'framework-2', '-framework', 'framework-1']

    result = pypkgconf.query_args('--libs framework-1 framework-2', env=lib1_env)
    assert result == ['-F/test/lib', '-framework', 'framework-2', '-framework', 'framework-1']
