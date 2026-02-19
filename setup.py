#!/usr/bin/env python3
"""
Setup script for building the C++ search engine extension
"""

from setuptools import setup, Extension
import pybind11
import sys

# C++ extension module
ext_modules = [
    Extension(
        'search_engine',
        sources=['search_engine.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++',
        extra_compile_args=['-std=c++17', '-O3', '-march=native', '-ffast-math'],
    ),
]

setup(
    name='sequencium',
    version='1.0.0',
    description='Sequencium game with optimized C++ search engine',
    ext_modules=ext_modules,
    zip_safe=False,
)
