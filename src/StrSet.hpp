// Copyright (c) Timur Iskhakov.
// Distributed under the terms of the MIT License.


#ifndef STRSET_HPP
#define STRSET_HPP

#include "AhoCorasick.hpp"
#include "SuffixTree.hpp"

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
    bool check_occurrence(std::vector<std::string> const &) const;
};

#endif //STRSET_HPP
