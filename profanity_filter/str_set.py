"""
Set of strings

Use to find word occurrence in sentence
"""

# Copyright (c) Timur Iskhakov.
# Distributed under the terms of the MIT License.

import re


class StrSet:
    class TrieNode:
        def __init__(self):
            self.links = {}
            self.term = False
            self.suffix_link = None

    def __init__(self, words_str):
        """
        :param words_str: :class:`str` string containing stopwords
        """
        self.root = StrSet.TrieNode()
        self.list = []

        patterns = re.sub("[^\w|-]", " ",  words_str).split()

        for __pattern in patterns:
            self.list.append(__pattern)
            pattern = ' ' + __pattern + ' '
            self.__add_pattern(pattern)

        self.__proceed_aho_corasick()

    def __add_pattern(self, pattern):
        node = self.root
        for symbol in pattern:
            node = node.links.setdefault(symbol, StrSet.TrieNode())
        node.term = True

    def __proceed_aho_corasick(self):
        queue = []

        for node in self.root.links.items():
            queue.append(node[1])
            node[1].suffix_link = self.root

        while queue:
            current_node = queue.pop(0)

            for key, node in current_node.links.items():
                queue.append(node)
                suffix = current_node.suffix_link
                while suffix is not None and key not in suffix.links:
                    suffix = suffix.suffix_link
                node.suffix_link = suffix.links[key] if suffix else self.root

    def check_occurrence(self, words):
        """Find out an occurrence of a word from the sentence in the dictionary.

        :param words: sentence to find occurrences
        :return: True if a word or a collocation in the sentence
                 occurrences in the dictionary
        """

        node = self.root
        sentence = ' ' + ' '.join(words) + ' '

        for symbol in sentence:
            while node is not None and symbol not in node.links:
                node = node.suffix_link
            if node is None:
                node = self.root
                continue
            node = node.links[symbol]
            if node.term:
                return True

        return False

    def empty(self):
        return not len(self.list)
