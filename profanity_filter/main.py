# Copyright (c) Timur Iskhakov.
# Distributed under the terms of the MIT License.


import argparse
import os.path
import sys

from profanity_filter.corpus import Corpus
from profanity_filter.str_set import StrSet
from profanity_filter.raw_text import RawText
from profanity_filter.ui_progress_bar import UIProgressBar


def __file_extension(filename):
    """Get the file extension.

    :param filename: File path
    :return: File extension
    """
    return os.path.splitext(filename)[1][1:]


def __count_lines(file):
    """Count lines in the file.

    :param file: Opened file (the pointer needs to be at the beginning)
    :return: Number of lines
    """
    lines = 0
    buf_size = 1024 * 1024
    read_f = file.read

    buf = read_f(buf_size)
    while buf:
        lines += buf.count('\n')
        buf = read_f(buf_size)
    file.seek(0)
    return lines + 1


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

    print('Preparing...', end='\r')

    run_corpus = (__file_extension(args.input[0].name) == 'vert' and args.type != 'text') or args.type == 'corpus'
    progress_bar = UIProgressBar('Corpus' if run_corpus else 'Text')

    if run_corpus:
        args.input[0].close()
        args.output[0].close()

        Corpus(args.input[0].name, args.output[0].name, args.stoplist.read(), progress_bar).proceed()
    else:
        progress_bar.init(__count_lines(args.input[0]))
        stop_set = StrSet(args.stoplist.read())
        RawText(args.input[0], args.output[0], stop_set, progress_bar).proceed()

    progress_bar.finish()


def entry_point():
    """Zero-argument entry point for use with setuptools/distribute."""
    raise SystemExit(main(sys.argv[1:]))


if __name__ == '__main__':
    entry_point()
