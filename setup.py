#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ez_repo import __version__

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requirements = [
    "wheel     >= 0.30.0",
    "boto3     >= 1.4.8",
    "ConfigObj >= 5.0.6",
    "colorlog  >= 3.1.0",
    "enum34    >= 1.1.6"
]

test_requirements = [
    "pytest >= 3.3.0"
]

setup(
    name='ez-repo',
    version=__version__,
    description="Command line tool to manage an artefact repository.",
    author="Jonathan Pigrée",
    author_email='jonathan.pigree@easymile.com',
    packages=[
        'ez_repo',
    ],
    package_dir={'ez_repo': 'ez_repo'},
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='artefact, repository, AWS S3',
    classifiers=[
        'Development Status :: {}'.format(__version__),
        'Intended Audience :: Developers',
        'License :: MIT',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts': [
            'ez-repo=ez_repo.main:main',
        ]
    }
)
