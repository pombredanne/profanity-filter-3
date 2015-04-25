"""
Corpus of texts
"""


# Copyright (c) Timur Iskhakov.
# Distributed under the terms of the MIT License.


from .file_streams import InputFileStream, OutputFileStream


class Corpus:
    def __init__(self, input_file_path, output_file_path, string_dict):
        """
        :param input_file_path: Corpus file path
        :param output_file_path: Output file path
        :param string_dict: Profanity dictionary
        """

        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.dict = string_dict

    def __proceed_sentence(self, input_stream):
        line = input_stream.get_next_line()
        lines, words = [], []

        while line[0] != '<':
            words.append(line.rstrip().split()[-1].split('-')[0])
            lines.append(line)
            line = input_stream.get_next_line()

        while line != '</s>\n':
            lines.append(line)
            line = input_stream.get_next_line()

        return self.dict.check_occurrence(words), lines

    def __proceed_xml(self, input_stream, output_stream):
        line = input_stream.get_next_line()

        while line:
            if line == '<s>\n':
                sentence = self.__proceed_sentence(input_stream)

                if sentence[0]:
                    output_stream.write('<s profanity="true">\n')
                else:
                    output_stream.write('<s>\n')

                output_stream.write(''.join(sentence[1]))
            else:
                output_stream.write(line)

            line = input_stream.get_next_line()

    def proceed(self):
        """Find out profanity sentences"""

        self.__proceed_xml(InputFileStream(self.input_file_path),
                           OutputFileStream(self.output_file_path))
