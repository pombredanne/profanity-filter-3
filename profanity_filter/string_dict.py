"""
Dictionary of strings

Use to find word occurrence in sentence
"""

# Copyright (c) Timur Iskhakov.
# Distributed under the terms of the MIT License.


class StringDict:
    class TrieNode:
        def __init__(self):
            self.links = {}
            self.term = False
            self.suffix_link = None

    def __init__(self, patterns):
        self.root = StringDict.TrieNode()

        for pattern in patterns:
            self.__add_pattern(pattern)

        self.__proceed_aho_corasick()

    def __add_pattern(self, pattern):
        node = self.root
        for symbol in pattern:
            node = node.links.setdefault(symbol, StringDict.TrieNode())
        node.term = True

    def __proceed_aho_corasick(self):
        queue = []
        for node in self.root.links.items():
            queue.append(node[1])
            node[1].suffix_link = self.root

        while not queue:
            current_node = queue.pop(0)

            for key, node in current_node.links.iteritems():
                queue.append(node)
                fail_node = current_node.fail
                while fail_node is not None and key not in fail_node.goto:
                    fail_node = fail_node.fail
                node.fail = fail_node.goto[key] if fail_node else self.root
                node.out += node.fail.out

    def check_occurrence(self, sentence):
        """
        :param sentence: sentence to find occurrences
        :return: True if a word or a collocation in the sentence
        occurrences in the dictionary
        """

        node = self.root
        sentence = sentence.replace(' ', '')

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
