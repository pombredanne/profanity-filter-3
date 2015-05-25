"""
Corpus of texts
"""


# Copyright (c) Timur Iskhakov.
# Distributed under the terms of the MIT License.


class Corpus:
    def __init__(self, input_stream, output_stream, stop_set):
        """
        :param input_stream: Corpus stream
        :param output_stream: Output stream
        :param stop_set: Profanity dictionary
        """

        self.input_stream = input_stream
        self.output_stream = output_stream
        self.stop_set = stop_set

    def __proceed_word(self, word):
        for part in reversed(word.split()):
            hyphen_pos = part.find('-')
            if hyphen_pos != -1:
                return part[:hyphen_pos]

    def __proceed_sentence(self, input_stream):
        line = input_stream.readline().rstrip()
        lines, words = [], []

        while line != '</s>':
            if line[0].isalpha():
                words.append(self.__proceed_word(line))
            lines.append(line)
            line = input_stream.readline().rstrip()

        return self.stop_set.check_occurrence(words), lines

    def __proceed_xml(self, input_stream, output_stream):
        line = input_stream.readline().rstrip()

        while line:
            if line == '<s>':
                sentence = self.__proceed_sentence(input_stream)

                if sentence[0]:
                    output_stream.write('<s profanity="true">\n')
                else:
                    output_stream.write('<s>\n')

                output_stream.write('\n'.join(sentence[1]) + '\n</s>\n')
            else:
                output_stream.write(line + '\n')

            line = input_stream.readline().rstrip()

    def proceed(self):
        """Find out profanity sentences."""

        self.__proceed_xml(self.input_stream, self.output_stream)
