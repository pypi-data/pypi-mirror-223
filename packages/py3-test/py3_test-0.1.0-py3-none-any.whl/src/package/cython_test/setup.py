# Created on: 2018/2/24 10:34
# Email: lijicong@163.com
# desc python setup.py build_ext --inplace

from distutils.core import setup

from Cython.Build import cythonize

setup(ext_modules=cythonize("helloworld.pyx"))
