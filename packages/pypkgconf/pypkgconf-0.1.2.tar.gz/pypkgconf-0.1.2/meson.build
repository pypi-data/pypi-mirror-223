project('pypkgconf',
    ['c'],
    license: 'Apache-2.0',
    meson_version: '>=1.1.0',
    version: '0.1.2',
)


libpkgconf = dependency('pkgconf', fallback: ['pkgconf', 'dep_libpkgconf'], version: '2.0.0')
libpkgconf_include = libpkgconf.get_variable('includedir', default_value: meson.global_source_root() / 'subprojects' / 'pkgconf')

fs = import('fs')
pymod = import('python')
py = pymod.find_installation(modules: ['cffi'], pure: false)

libpkgconf_c = '_libpkgconf.c'

c_bindings = custom_target(
    'libpkgconf_c',
    command: [py, meson.current_source_dir() / 'cffibuild.py', libpkgconf_include, '@OUTPUT@'],
    output: [libpkgconf_c],
    depend_files: ['cffibuild.py'],
)

pkgconf = subproject('pkgconf')
cdata = pkgconf.get_variable('cdata')
build_static = pkgconf.get_variable('build_static')

subdir('pypkgconf')

pytest = pymod.find_installation(modules: ['pytest'], required: false)
if pytest.found()
    pytest_env = environment(
        {
            'PYTHONPATH': meson.current_build_dir(),
            'PKG_DEFAULT_PATH': cdata.get_unquoted('PKG_DEFAULT_PATH')
        }
    )

    test(
        'pypkgconf',
        pytest,
        args: [
            '-m', 'pytest',
            '-vv',
            # '-o log_cli=true', '--log-cli-level=DEBUG',
            meson.current_source_dir() / 'tests'],
        env: pytest_env,
        depends: test_python_files,
    )
else
    message('Skipping Python tests as pytest was not found.')
endif
