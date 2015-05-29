/**
 * Suffix tree for similarity checks
 */


// Copyright (c) Timur Iskhakov.
// Distributed under the terms of the MIT License.


#ifndef SUFFIX_TREE_HPP
#define SUFFIX_TREE_HPP

#include <string>

class SuffixTree {

public:
    SuffixTree(std::string const &);

    static bool similar(SuffixTree const &, SuffixTree const &);
};


#endif //SUFFIX_TREE_HPP
