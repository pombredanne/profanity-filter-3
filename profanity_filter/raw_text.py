"""
Raw text
"""


# Copyright (c) Timur Iskhakov.
# Distributed under the terms of the MIT License.


from .file_streams import InputFileStream, OutputFileStream

import pymorphy2


class RawText:
    def __init__(self, input_file_path, output_file_path, string_dict):
        """
        :param input_file_path: Text file path
        :param output_file_path: Output file path
        :param string_dict: Profanity dictionary
        """

        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.dict = string_dict

        self.alphabet = ('а', )
        self.morph = pymorphy2.MorphAnalyzer()
        self.stops = ('...', '!..', '?..', '!', '?', '.')

    def __normalize(self, token):
        try:
            gram_info = self.morph.parse(token)
            return gram_info[0].normal_form
        except:
            return token

    def __proceed_sentence(self, sentence):
        words = []
        curr_word = ''

        for ch in sentence:
            if ch.isalpha():
                curr_word += ch
            elif curr_word:
                words.append(self.__normalize(curr_word))
                curr_word = ''

        return not self.dict.check_occurrence(words)

    def __get_stop_pos(self, part):
        pos = (-1, 0)

        for stop in self.stops:
            curr_pos = part.find(stop)
            if curr_pos != -1 and (pos[0] == -1 or pos[0] > curr_pos):
                pos = (curr_pos, len(stop))
        return pos[0] + pos[1]

    def __proceed_part(self, part, output_stream):
        stop_pos = self.__get_stop_pos(part)
        while stop_pos != -1:
            if self.__proceed_sentence(part[:stop_pos]):
                output_stream.write(part[:stop_pos])
            part = part[stop_pos:]
            stop_pos = self.__get_stop_pos(part)

        return part

    def __proceed_text(self, input_stream, output_stream):
        collected_line = ''
        line = input_stream.get_next_line()

        while line:
            collected_line = self.__proceed_part(collected_line, output_stream)
            line = input_stream.get_next_line()
            collected_line += line
        self.__proceed_part(collected_line, output_stream)

    def proceed(self):
        """Copy text without profanity sentences"""

        self.__proceed_text(InputFileStream(self.input_file_path),
                            OutputFileStream(self.output_file_path))
