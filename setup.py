# Copyright (c) Timur Iskhakov.
# Distributed under the terms of the MIT License.


import pip
from setuptools import setup, Extension

from profanity_filter import metadata


install_reqs = pip.req.parse_requirements('requirements.txt', session=pip.download.PipSession())

setup(
    name=metadata.project,
    version=metadata.version,
    author=metadata.authors_string,
    author_email=metadata.emails[0],
    description=metadata.description,
    license=metadata.license,
    url=metadata.url,
    ext_modules=[Extension(
        metadata.package + '.str_set',
        ['src/package.cpp', 'src/AhoCorasick.cpp', 'src/SuffixTree.cpp', 'src/StrSet.cpp'],
        libraries=['boost_python3'],
        extra_compile_args=["-std=c++11"]
    )],
    packages=[metadata.package],
    entry_points={
        'console_scripts': [metadata.project + '=' + metadata.package + '.main:entry_point'],
    },
    install_requires=[str(ir.req) for ir in install_reqs],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',
    ],
)
