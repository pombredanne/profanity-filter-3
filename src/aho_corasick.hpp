// Copyright (c) Timur Iskhakov.
// Distributed under the terms of the MIT License.


#ifndef AHO_CORASICK_HPP
#define AHO_CORASICK_HPP

#include <map>
#include <string>
#include <vector>


class AhoCorasick {
    struct TrieNode {
        std::map<char const, TrieNode *> links;
        TrieNode *fail;//, *term;
        bool term;

    public:
        TrieNode(TrieNode *fail_node = nullptr) :
                fail(fail_node),
                //term(nullptr),
                term(false)
        { }

        TrieNode * get_link(char ch) const {
            auto iter = links.find(ch);
            return (iter != links.cend() ? iter->second : nullptr);
        }
    };

    TrieNode *root_;

    void add_pattern_(std::string const &);
    void proceed_aho_corasick_();
    TrieNode const * step_(TrieNode const *, char) const;

public:
    AhoCorasick() : root_(nullptr) {}
    AhoCorasick(std::vector<std::string> const &);

    bool occur(std::string const &) const;
};

#endif //AHO_CORASICK_HPP
