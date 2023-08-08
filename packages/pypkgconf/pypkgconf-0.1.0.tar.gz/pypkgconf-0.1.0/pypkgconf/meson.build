# This subdir is only to ensure the extension module is generated
# inside a directory whose name matches the final installation dir
# to allow in-tree testing

package_name = 'pypkgconf'
python_files = ['__init__.py', 'callbacks.py', 'clilike.py', 'constants.py', 'logger.py', 'util.py']

test_python_files = []
foreach f: python_files
    test_python_files += fs.copyfile(f)
endforeach

test_python_files += py.extension_module(
    '_libpkgconf',
    [c_bindings],
    dependencies: [libpkgconf],
    c_args: [
        '-D_CFFI_NO_LIMITED_API',  # workaround until meson support it
        build_static,  # workaround since it is not included in declare_dependency
    ],
    install: true,
    subdir: package_name,
)

py.install_sources(
    python_files,
    subdir: package_name
)

if get_option('default_library') != 'static' and host_machine.system() == 'windows'

    error('dynamic linking is not supported yet on Windows.')

    # On Windows, the pkgconf dll must be side-by-side with the bindings
    # to be found when testing

endif
