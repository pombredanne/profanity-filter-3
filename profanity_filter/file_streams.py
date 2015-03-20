"""
File streams

Use for big files
"""


# Copyright (c) Timur Iskhakov.
# Distributed under the terms of the MIT License.


class InputFileStream:
    """File input stream storing one line at the same time"""

    def __init__(self, file_path):
        try:
            self.file = open(file_path, 'r')
            self.line = ''
        except (OSError, IOError):
            print('An error occurred while opening file', file_path)
            print('Check if the file exists and is readable')

        self.last = None

    def __del__(self):
        self.file.close()

    def get_next_line(self):
        return self.file.readline()


class OutputFileStream:
    """File output stream
    File class shell to enhance readability
    """

    def __init__(self, file_path):
        try:
            self.file = open(file_path, 'w')
        except (OSError, IOError):
            print('An error occurred while opening file', file_path)
            print('Check if the file exists and is writeable')

        self.last = None

    def __del__(self):
        self.file.close()

    def write(self, line):
        self.file.write(line)
