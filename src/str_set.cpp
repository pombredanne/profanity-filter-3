// Copyright (c) Timur Iskhakov.
// Distributed under the terms of the MIT License.


#include "str_set.hpp"


std::regex const StrSet::word_regex_("[\\абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ-]+");

StrSet::StrSet(std::string const &get_str, bool complex_analysis) : complex_(complex_analysis) {
    std::string str = get_str;
    std::vector<std::string> words;
    std::smatch words_match;

    while (std::regex_search(str, words_match, word_regex_)) {
        words.push_back(words_match.str());
        suffix_trees_.push_back(SuffixTree(words_match.str()));
        str = words_match.suffix().str();
    }

    trie_ = AhoCorasick(words);
}

bool StrSet::check_occurrence(boost::python::list const &get_words) const {
    boost::python::ssize_t len = boost::python::len(get_words);
    std::vector<std::string> words(len);

    for (boost::python::ssize_t i = 0; i != len; ++i) {
        words[i] = boost::python::extract<std::string>(get_words[i]);
    }

    std::string all_words = " ";
    for (auto const &word : words) {
        all_words += word + " ";
    }

    if (trie_.occurre(all_words)) {
        return true;
    }

    if (complex_) {
        for (auto const &word : words) {
            for (auto const &tree : suffix_trees_) {
                if (SuffixTree::similar(SuffixTree(word), tree)) {
                    return true;
                }
            }
        }
    }

    return false;
}
