"""
Raw text
"""

# Copyright (c) Timur Iskhakov.
# Distributed under the terms of the MIT License.


import pymorphy2


class RawText:
    def __init__(self, input_stream, output_stream, stop_set, progress_bar):
        """
        :param input_stream: Text stream
        :param output_stream: Output stream
        :param stop_set: Profanity dictionary
        :param progress_bar: :class:`UIProgressBar` Progress bar
        """

        self.input_stream = input_stream
        self.output_stream = output_stream
        self.stop_set = stop_set
        self.progress_bar = progress_bar

        self.morph = pymorphy2.MorphAnalyzer()
        self.stops = ('.', '!', '?', '…')

    def __normalize(self, token):
        """Normalize the token.

        :param token: Token containing the word
        :return: The word infinitive
        """

        return self.morph.parse(token)[0].normal_form

    def __proceed_sentence(self, sentence):
        """Proceed the sentence.

        :param sentence: The sentence
        :return: Absence of obscene vocabulary
        """

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
        """Find a sentence end position.

        :param part: Part of the text
        :return: A sentence end position or -1 if not found
        """

        # FIX ME

        pos = -1
        for ind, ch in enumerate(part):
            if ch in self.stops:
                pos = ind + 1
            elif pos != -1:
                return pos
        return pos

    def __proceed_part(self, part, output_stream):
        """Proceed text part.

        :param part: Part of the text
        :param output_stream: Output stream
        :return: Remaining part of the text
        """

        stop_pos = self.__get_stop_pos(part)
        while stop_pos != -1:
            start_pos = 0
            while part[start_pos] in ' \t':
                start_pos += 1
            output_stream.write(part[:start_pos])

            if self.__proceed_sentence(part[start_pos:stop_pos]):
                output_stream.write(part[start_pos:stop_pos])

            part = part[stop_pos:]
            stop_pos = self.__get_stop_pos(part)

        return part

    def __proceed_text(self, input_stream, output_stream):
        """Proceed the text.

        :param input_stream: Input stream
        :param output_stream: Output stream
        """

        collected_line = ''
        line = input_stream.readline()

        while line:
            collected_line = self.__proceed_part(collected_line, output_stream)
            self.progress_bar.step()
            line = input_stream.readline()
            collected_line += line
        self.__proceed_part(collected_line, output_stream)

    def proceed(self):
        """Copy text without profanity sentences."""

        if self.stop_set.empty():
            print('Stoplist is empty!')

        self.__proceed_text(self.input_stream, self.output_stream)
