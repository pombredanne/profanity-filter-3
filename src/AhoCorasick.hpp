// Copyright (c) Timur Iskhakov.
// Distributed under the terms of the MIT License.


#ifndef AHOCORASICK_HPP
#define AHOCORASICK_HPP

#include <map>
#include <string>
#include <vector>


class AhoCorasick {
    struct TrieNode {
        std::map<char const, TrieNode *> links;
        TrieNode *fail, *term;
        bool terminal;

    public:
        TrieNode(TrieNode *fail_node = nullptr) :
                fail(fail_node),
                term(nullptr),
                terminal(false)
        { }

        /*
        TrieNode * get_link(char ch) const {
            auto iter = links.find(ch);
            return (iter != links.cend() ? *iter : nullptr);
        }

        TrieNode * set_default(char ch)
        */
    };

    TrieNode *root_;

    void add_pattern_(std::string const &);
    void proceed_aho_corasick_();

public:
    AhoCorasick() : root_(nullptr) {}
    AhoCorasick(std::vector<std::string> const &);

    bool occurre(std::string const &) const;
};

#endif //AHOCORASICK_HPP
