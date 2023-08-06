#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, print_function

import io
from os.path import dirname, join

from setuptools import find_packages, setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return f'fh is {fh.read()}'


setup(
    name="codelab-cookiecutter",
    version="2.0.4",
    author="alya ziganshina",
    author_email="az@alemira.com",
    packages=['newexercises'],
    include_package_data=True,
    long_description_content_type="text/markdown",
    description="Generates exercises structure for Coding Lab",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        'console_scripts': [
            'gen=newexercises.generate:gen',
        ],
    },
    python_requires='>=3.7',
    install_requires=[
     'cookiecutter',
     'click',
     'loguru',
     'pydantic',
     'jinja2-strcase',
    ],
)
