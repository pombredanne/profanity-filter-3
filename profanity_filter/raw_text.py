"""
Raw text
"""


# Copyright (c) Timur Iskhakov.
# Distributed under the terms of the MIT License.


import pymorphy2


class RawText:
    def __init__(self, input_stream, output_stream, stop_set):
        """
        :param input_stream: Text stream
        :param output_stream: Output stream
        :param stop_set: Profanity dictionary
        """

        self.input_stream = input_stream
        self.output_stream = output_stream
        self.stop_set = stop_set

        self.alphabet = ('а', )
        self.morph = pymorphy2.MorphAnalyzer()
        self.stops = ('.', '!', '?', '…')

    @staticmethod
    def __levenshtein_distance(a, b):
        """Calculates the Levenshtein distance.

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
        pos = -1
        for ind, ch in enumerate(part):
            if ch in self.stops:
                pos = ind + 1
            elif pos != -1:
                return pos
        return pos

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
        line = input_stream.readline()

        while line:
            collected_line = self.__proceed_part(collected_line, output_stream)
            line = input_stream.readline()
            collected_line += line
        self.__proceed_part(collected_line, output_stream)

    def proceed(self):
        """Copy text without profanity sentences."""

        if self.stop_set.empty():
            print('Stopset is empty!')

        self.__proceed_text(self.input_stream, self.output_stream)
