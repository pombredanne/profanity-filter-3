// Copyright (c) Timur Iskhakov.
// Distributed under the terms of the MIT License.


#ifndef SUFFIXTREE_HPP
#define SUFFIXTREE_HPP

#include <string>

class SuffixTree {

public:
    SuffixTree(std::string const &);

    static bool similar(SuffixTree const &, SuffixTree const &);
};


#endif //SUFFIXTREE_HPP
