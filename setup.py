#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""

from setuptools import setup, find_packages

# with open('README.rst') as readme_file:
#     readme = readme_file.read()
readme = ''

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['graphql-core>=2.0']

setup_requirements = [
    'pytest-runner',
    # TODO(graphql-python): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest', 'graphene>=2.0'
    # TODO: put package test requirements here
]

setup(
    name='graphql_env',
    version='0.1.0',
    description=
    "The package for setting up a GraphQL Environment with custom backends",
    long_description=readme + '\n\n' + history,
    author="Syrus Akbary",
    author_email='me@syrusakbary.com',
    url='https://github.com/graphql-python/graphql-env',
    packages=find_packages(include=['graphql_env']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='graphql_env',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
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
    tests_require=test_requirements,
    setup_requires=setup_requirements, )
