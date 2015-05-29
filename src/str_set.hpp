/**
 * Set of strings.
 */

// Copyright (c) Timur Iskhakov.
// Distributed under the terms of the MIT License.


#ifndef STR_SET_HPP
#define STR_SET_HPP

#include <boost/python.hpp>
#include "aho_corasick.hpp"
#include "suffix_tree.hpp"

#include <regex>
#include <string>
#include <vector>


class StrSet {
    /**
     * A word in Russian regex.
     */
    static std::regex const word_regex_;

    /**
     * Suffix tree for each word in the set.
     */
    std::vector<SuffixTree> suffix_trees_;

    /**
     * An AhoCorasick trie for quick check.
     */
    AhoCorasick trie_;

    /**
     * Designates proceeding a similarity check
     */
    bool complex_;

public:
    StrSet(std::string const &, bool);
    bool check_occurrence(boost::python::list const &) const;

    /**
     * Establishes whether the set is empty.
     *
     * @return True if the set is empty
     */
    bool empty() const {
        return suffix_trees_.empty();
    }
};

#endif //STR_SET_HPP
