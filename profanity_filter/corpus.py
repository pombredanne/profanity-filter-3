"""
Corpus of texts
"""


# Copyright (c) Timur Iskhakov.
# Distributed under the terms of the MIT License.


class Corpus:
    def __init__(self, input_stream, output_stream, stop_set, progress_bar):
        """
        :param input_stream: Corpus stream
        :param output_stream: Output stream
        :param stop_set: Profanity dictionary
        :param progress_bar: :class:`UIProgressBar` Progress bar
        """

        self.input_stream = input_stream
        self.output_stream = output_stream
        self.stop_set = stop_set
        self.progress_bar = progress_bar

    @staticmethod
    def __proceed_word(word):
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

            self.progress_bar.step()
            line = input_stream.readline().rstrip()

        return self.stop_set.check_occurrence(words), lines

    def __proceed_xml(self, input_stream, output_stream):
        line = input_stream.readline().rstrip()

        while line:
            if line == '<s>':
                self.progress_bar.step()
                sentence = self.__proceed_sentence(input_stream)

                if sentence[0]:
                    output_stream.write('<s profanity="true">\n')
                else:
                    output_stream.write('<s>\n')

                output_stream.write('\n'.join(sentence[1]) + '\n</s>\n')
            else:
                output_stream.write(line + '\n')

            self.progress_bar.step()
            line = input_stream.readline().rstrip()

    def proceed(self):
        """Find out profanity sentences."""

        if self.stop_set.empty():
            print('Stopset is empty!')

        self.__proceed_xml(self.input_stream, self.output_stream)
