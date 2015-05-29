# Copyright (c) Timur Iskhakov.
# Distributed under the terms of the MIT License.


import argparse
import distutils.sysconfig
import fileinput
import functools
import hashlib
import os
import pip
import shutil
import setuptools
import subprocess
import sys
import tarfile
import urllib.request

from profanity_filter import metadata


def __md5_sum(filename):
    with open(filename, mode='rb') as f:
        hasher = hashlib.md5()
        for buf in iter(functools.partial(f.read, 128), b''):
            hasher.update(buf)
    return hasher.hexdigest()


def __replace_in_file(filename, search, replace):
    for line in fileinput.input(filename, inplace=True):
        print(line.replace(search, replace), end='')


# Require Python3
if len(sys.argv) != 1 and '-h' not in sys.argv and '--help' not in sys.argv and '--help-commands' not in sys.argv:
    if sys.version_info.major != 3:
        print('Please run with python3')
        exit(0)


install_reqs = pip.req.parse_requirements('requirements.txt', session=pip.download.PipSession())

compile_args = ['-std=c++11']
library_dirs = []
if sys.platform == 'darwin':
    compile_args.append('-stdlib=libc++')


argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('--with-boost', action='store_true', help='Download and use local boost')
args, unknown = argparser.parse_known_args()
sys.argv = [sys.argv[0]] + unknown


# Boost installation
if args.with_boost:
    print('Boost will be prepared now. It might take a while.')

    compile_args.append('-Iboost_1_58_0')
    library_dirs.append('stage-python3/lib')

    boost_url = 'https://downloads.sourceforge.net/project/boost/boost/1.58.0/boost_1_58_0.tar.bz2'
    boost_name = 'boost_1_58_0.tar.bz2'
    boost_md5 = 'b8839650e61e9c1c0a89f371dd475546'
    boost_dir = 'boost_1_58_0'

    if not (os.path.isfile(boost_name) and __md5_sum(boost_name) == boost_md5):
        print('Downloading', boost_name)

        with urllib.request.urlopen(boost_url) as response, open(boost_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

    if os.path.exists(boost_dir):
        shutil.rmtree(boost_dir, ignore_errors=True)

    print('Extracting', boost_name)
    tar = tarfile.open(boost_name)
    tar.extractall()
    tar.close()

    print('Building')
    os.chdir(boost_dir)

    # Disable python detection in bootstrap.sh; it guesses the wrong include directory
    # for Python 3 headers, so we configure python manually in user-config.jam below.
    __replace_in_file('bootstrap.sh', 'using python', '#using python')

    with open('user-config.jam', 'w') as user_config:
        config = 'using python : 3.' + str(sys.version_info.minor) + '\n' +\
                 '             : python3\n' +\
                 '             : ' + distutils.sysconfig.get_python_inc(True) + '\n' +\
                 '             : ' + sys.prefix + ' ;'
        user_config.write(config)

    subprocess.call([
        './bootstrap.sh',
        '--prefix=../boost-python',
        '--libdir=../boost-python/lib',
        '--with-libraries=python',
        '--with-python=python3',
        '--with-python-root=' + sys.prefix,
    ])

    subprocess.call([
        './b2',
        '--build-dir=../boost-build-python3',
        '--stagedir=../boost-stage-python3',
        'python=3.' + str(sys.version_info.minor),
        '--prefix=../boost-python',
        '--libdir=../boost-python/lib',
        '-d2',
        '-j4',
        '--layout=tagged',
        '--user-config=user-config.jam',
        'threading=multi,single',
        'link=shared,static',
    ])

    os.chdir('..')


setuptools.setup(
    name=metadata.project,
    version=metadata.version,
    author=metadata.authors_string,
    author_email=metadata.emails[0],
    description=metadata.description,
    license=metadata.license,
    url=metadata.url,
    ext_modules=[setuptools.Extension(
        metadata.package + '.str_set',
        ['src/package.cpp', 'src/aho_corasick.cpp', 'src/suffix_tree.cpp', 'src/str_set.cpp'],
        libraries=['boost_python3'] if args.with_boost else [],
        extra_compile_args=compile_args,
        library_dirs=library_dirs,
    )],
    include_package_data=True,
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
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',
    ],
)
