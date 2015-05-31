// Copyright (c) Timur Iskhakov.
// Distributed under the terms of the MIT License.


#include "str_set.hpp"


std::regex const StrSet::word_regex_("[абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ-]+");

StrSet::StrSet(std::string const &get_str) : words_count_(0) {
    std::string str = get_str;
    std::smatch words_match;

    while (std::regex_search(str, words_match, word_regex_)) {
        if (trie_.add_pattern(" " + words_match.str() + " ")) {
            ++words_count_;

#ifdef SIMILARITIES_ANALYSIS
            suffix_trees_.emplace_back(SuffixTree(words_match.str()));
#endif //SIMILARITIES_ANALYSIS

        }

        str = words_match.suffix().str();
    }
}

#ifdef BOOST_PYTHON

bool StrSet::check_occurrence_python(boost::python::list const &get_words) const {
    boost::python::ssize_t len = boost::python::len(get_words);
    std::vector<std::string> words(len);

    for (boost::python::ssize_t i = 0; i != len; ++i) {
        words[i] = boost::python::extract<std::string>(get_words[i]);
    }

    return check_occurrence(words);
}

#endif //BOOST_PYTHON

bool StrSet::check_occurrence(std::vector<std::string> const &words) const {
    std::string all_words = " ";
    for (auto const &word : words) {
        all_words += word + " ";
    }

    if (trie_.occur(all_words)) {
        return true;
    }

#ifdef SIMILARITIES_ANALYSIS

    for (auto const &word : words) {
        for (auto const &tree : suffix_trees_) {
            if (SuffixTree::similar(SuffixTree(word), tree)) {
                return true;
            }
        }
    }

#endif //SIMILARITIES_ANALYSIS

    return false;
}
