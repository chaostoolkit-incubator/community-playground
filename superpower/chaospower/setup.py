#!/usr/bin/env python
"""chaostoolkit-power extension builder and installer"""
import sys
import io

import setuptools

sys.path.insert(0, ".")
from chaospower import __version__
sys.path.remove(".")

name = 'chaostoolkit-power'
desc = 'Chaos Toolkit Extension for the SuperPower services'

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: Freely Distributable',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: Implementation',
    'Programming Language :: Python :: Implementation :: CPython'
]
author = "chaostoolkit Team"
author_email = 'contact@chaostoolkit.org'
url = 'http://chaostoolkit.org'
license = 'Apache License Version 2.0'
packages = [
    'chaospower'
]


setup_params = dict(
    name=name,
    version=__version__,
    description=desc,
    long_description=desc,
    classifiers=classifiers,
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    packages=packages,
    include_package_data=True,
    install_requires=[
        "chaostoolkit-lib",
        "requests"
    ],
    python_requires='>=3.5.*'
)


def main():
    """Package installation entry point."""
    setuptools.setup(**setup_params)


if __name__ == '__main__':
    main()