#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pip.req import parse_requirements
from os import path

base_path = path.dirname(path.realpath(__file__))
requirements_path = path.join(base_path, 'requirements.txt')
requirements_test_path = path.join(base_path, 'requirements_test.txt')
install_reqs = parse_requirements(requirements_path, session=False)
install_reqs_test = parse_requirements(requirements_test_path, session=False)


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [str(ir.req) for ir in install_reqs]
test_requirements = [str(ir.req) for ir in install_reqs_test]

setup(
    name='doyle',
    version='0.1.0',
    description="doyle is a tool for creating and tracking bug reports, issues, and internal notes in code.",
    long_description=readme + '\n\n' + history,
    author="Martin Garcia",
    author_email='newluxfero@gmail.com',
    url='https://github.com/magarcia/doyle',
    packages=[
        'doyle',
    ],
    package_dir={'doyle':
                 'doyle'},
    include_package_data=True,
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        doyle=doyle:cli
    ''',
    license="ISCL",
    zip_safe=False,
    keywords='doyle',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
