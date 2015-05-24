"""
Raw text
"""


# Copyright (c) Timur Iskhakov.
# Distributed under the terms of the MIT License.


from .file_streams import InputFileStream, OutputFileStream

import pymorphy2


class RawText:
    def __init__(self, input_file_path, output_file_path, stop_set):
        """
        :param input_file_path: Text file path
        :param output_file_path: Output file path
        :param stop_set: Profanity dictionary
        """

        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.stop_set = stop_set

        self.alphabet = ('а', )
        self.morph = pymorphy2.MorphAnalyzer()
        self.stops = ('...', '…', '!..', '?..', '?!', '!', '?', '.')

    @staticmethod
    def __levenshtein_distance(a, b):
        """Calculates the Levenshtein distance

        :param a: :class:`str` first string
        :param b: :class:`str` second string
        :return: Levenshtein distance
        """

        n, m = len(a), len(b)
        if n > m:
            a, b = b, a
            n, m = m, n

        current_row = range(n + 1)
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
                if a[j - 1] != b[i - 1]:
                    change += 1
                current_row[j] = min(add, delete, change)

        return current_row[n]

    def __normalize(self, token):
        # Yeah, this is fun
        if token[:4] == 'пидо':
            return 'пидор'

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

        return not self.stop_set.check_occurrence(words)

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
            start_pos = 0
            while not part[start_pos].isalpha():
                start_pos += 1
            output_stream.write(part[:start_pos])

            if self.__proceed_sentence(part[start_pos:stop_pos]):
                output_stream.write(part[start_pos:stop_pos])

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
