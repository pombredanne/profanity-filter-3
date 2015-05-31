/**
 * Set of strings.
 */

// Copyright (c) Timur Iskhakov.
// Distributed under the terms of the MIT License.


#ifndef STR_SET_HPP
#define STR_SET_HPP

#ifdef BOOST_PYTHON
#include <boost/python.hpp>
#endif //BOOST_PYTHON

#include "aho_corasick.hpp"

#ifdef SIMILARITIES_ANALYSIS
#include "suffix_tree.hpp"
#endif //SIMILARITIES_ANALYSIS

#include <regex>
#include <string>
#include <vector>


class StrSet {
    /**
     * A word in Russian regex.
     */
    static std::regex const word_regex_;

    /*
     * Number of unique words in the set.
     */
    size_t words_count_;

    /**
     * An AhoCorasick trie for quick check.
     */
    AhoCorasick trie_;

#ifdef SIMILARITIES_ANALYSIS

    /**
     * Suffix tree for each word in the set.
     */
    std::vector<SuffixTree> suffix_trees_;

#endif //SIMILARITIES_ANALYSIS

public:
    /**
     * A constructor.
     * Make a set of strings.
     *
     * @param get_str String containing words
     * @param complex_analysis True for checking for similarities
     */
    StrSet(std::string const &);

    /**
     * Checks occurrence or similarity in the set.
     * @param get_words Vector of words
     */
    bool check_occurrence(std::vector<std::string> const &) const;

#ifdef BOOST_PYTHON

    /**
     * Checks occurrence or similarity in the set.
     * @param get_words List of words
     */
    bool check_occurrence_python(boost::python::list const &) const;

#endif //BOOST_PYTHON

    /**
     * Establishes whether the set is empty.
     *
     * @return True if the set is empty
     */
    bool empty() const {
        return !words_count_;
    }
};

#endif //STR_SET_HPP
