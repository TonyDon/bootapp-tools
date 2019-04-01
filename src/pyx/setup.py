import setuptools
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext

ext_modules = [Extension("hello",
                         ["hello.pyx"],
                          library_dirs=[r'C:\app\Python36'],
                         extra_compile_args=['-w'])
                         ]

#python setup.py build_ext --inplace
setup(
    name = "Hellopyx",
    version = '1.0',
    cmdclass = {'build_ext': build_ext},
    description = 'hello pyx',
    ext_modules = cythonize(ext_modules, compiler_directives={'language_level': 3}),
)