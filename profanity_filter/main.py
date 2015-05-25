# Copyright (c) Timur Iskhakov.
# Distributed under the terms of the MIT License.


import argparse
import os.path
import sys

from str_set import StrSet
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
    parser.add_argument('--stoplist',
                        default='resources/stoplist.txt',
                        type=argparse.FileType('r'),
                        help='Custom stoplist file')

    args = parser.parse_args(argv)
    stop_set = StrSet(map(str.rstrip, args.stoplist.readlines()))

    if (__file_extension(args.input[0].name) == 'vert' and args.type != 'text') or args.type == 'corpus':
        Corpus(args.input[0], args.output[0], stop_set).proceed()
    else:
        RawText(args.input[0], args.output[0], stop_set).proceed()


def entry_point():
    """Zero-argument entry point for use with setuptools/distribute."""
    raise SystemExit(main(sys.argv[1:]))


if __name__ == '__main__':
    entry_point()
