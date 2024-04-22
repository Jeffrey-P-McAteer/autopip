


from setuptools import setup, Extension

# Our module is an extension module since it is C code.

pythonIteratorModule = Extension(
  'python_iterator_module',
  sources = ['python_iterator_module.cpp'],
  extra_compile_args = ['-static-libstdc++'],
  extra_link_args = ['-static-libstdc++']
)

# The package name doesn't affect the name of the module created.

setup(name = 'python_iterator_module', ext_modules = [pythonIteratorModule])

