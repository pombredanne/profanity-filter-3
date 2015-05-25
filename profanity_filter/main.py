# Copyright (c) Timur Iskhakov.
# Distributed under the terms of the MIT License.


import argparse
import os.path
import sys

from str_set import set_from_file
from corpus import Corpus
from raw_text import RawText


def __file_extension(filename):
    return os.path.splitext(filename)[1][1:]


def main(argv):
    """Program entry point.

    :param argv: command-line arguments
    :type argv: :class:`list`
    """

    parser = argparse.ArgumentParser(description='Clear profanity from the text.')
    parser.add_argument('input',
                        nargs=1,
                        type=argparse.FileType('r'),
                        help='Input file')
    parser.add_argument('output',
                        type=argparse.FileType('w'),
                        nargs=1,
                        help='Output destination')
    parser.add_argument('--type',
                        choices=['corpus', 'text'],
                        nargs='?',
                        help='Input file type (vert is corpus by default)')

    args = parser.parse_args(argv)

    stop_set = set_from_file('resources/stoplist.txt')

    if (__file_extension(args.input[0].name) == 'vert' and args.type != 'text') or args.type == 'corpus':
        Corpus(args.input[0], args.output[0], stop_set).proceed()
    else:
        RawText(args.input[0], args.output[0], stop_set).proceed()


def entry_point():
    """Zero-argument entry point for use with setuptools/distribute."""
    raise SystemExit(main(sys.argv[1:]))


if __name__ == '__main__':
    entry_point()
