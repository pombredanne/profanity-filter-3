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
    static std::regex const word_regex_;

    std::vector<SuffixTree> suffix_trees_;
    AhoCorasick trie_;
    bool complex_;

public:
    StrSet(std::string const &, bool);
    bool check_occurrence(boost::python::list const &) const;

    bool empty() const {
        return suffix_trees_.empty();
    }
};

#endif //STR_SET_HPP
