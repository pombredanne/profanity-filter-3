# Copyright (c) Timur Iskhakov.
# Distributed under the terms of the MIT License.


import argparse
import sys

from filter import metadata

def main(argv):
    """Program entry point.

    :param argv: command-line arguments
    :type argv: :class:`list`
    """

    parser = argparse.ArgumentParser(description='Clear profanity from the text.')

    parser.add_argument('corpus',
                        action='store',
                        type=argparse.FileType('r'),
                        nargs=1,
                        help='Corpus file')

    args = parser.parse_args(argv)


def entry_point():
    """Zero-argument entry point for use with setuptools/distribute."""
    raise SystemExit(main(sys.argv[1:]))


if __name__ == '__main__':
    entry_point()
