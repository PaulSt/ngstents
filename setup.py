#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from skbuild import setup
from setuptools_scm import get_version
import sys

_cmake_args = []
version = get_version().split('+')[0]

ngsolve_version = '6.2.2402'
install_requires = [ 'ngsolve >= '+ngsolve_version, 'matplotlib' ] 

setup(
    name='ngstents',
    version=version,
    author='Jay Gopalakrishnan',
    author_email='gjay@pdx.edu',
    description='Spacetime tent facilities for solving hyperbolic equations',
    long_description='This ngstents package is a c++ extension of the NGSolve finite element library, designed to ease experimentation with solvers based on spacetime tents for hyperbolic systems. A python front-end allows new equations (linear or nonlinear conservation laws) to be solved by easily defining required fluxes and numerical fluxes in a few lines of code.',
    url="https://github.com/jayggg/ngstents",
    license="LGPL2.1",
    install_requires=install_requires,
    packages=["ngstents"],
    package_dir={"ngstents": "src"},
    cmake_args=_cmake_args,
    cmake_source_dir='src',
)
