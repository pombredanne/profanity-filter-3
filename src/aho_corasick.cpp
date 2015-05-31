// Copyright (c) Timur Iskhakov.
// Distributed under the terms of the MIT License.


#include "aho_corasick.hpp"

#include <queue>


AhoCorasick::~AhoCorasick() {
    delete_node_(root_);
}

void AhoCorasick::delete_node_(AhoCorasick::TrieNode *node) {
    for (auto link : node->links) {
        delete_node_(link.second);
    }
    delete node;
}

AhoCorasick::TrieNode const * AhoCorasick::step_(TrieNode const *node, char ch) const {
    while (node) {
        TrieNode const *candidate = node->get_link(ch);
        if (candidate) {
            return candidate;
        }
        node = node->fail;
    }
    return root_;
}

bool AhoCorasick::add_pattern(std::string const &pattern) {
    TrieNode *curr = root_;
    for (char ch : pattern) {
        TrieNode *child = curr->get_link(ch);
        if (!child) {
            child = new TrieNode(root_);
            curr->links[ch] = child;
        }
        curr = child;
    }

    bool unique = !curr->term;
    curr->term = true;
    return unique;
}

void AhoCorasick::proceed_aho_corasick() {
    std::queue<TrieNode *> queue;
    queue.push(root_);

    while (!queue.empty()) {
        TrieNode *curr = queue.front();
        queue.pop();

        for (auto link : curr->links) {
            char symbol = link.first;
            TrieNode *child = link.second;

            TrieNode *temp = curr->fail;
            while (temp) {
                TrieNode *candidate = temp->get_link(symbol);
                if (candidate) {
                    child->fail = candidate;
                    break;
                }
                temp = temp->fail;
            }

            queue.push(child);
        }
    }
}

bool AhoCorasick::occur(std::string const &str) const {
    TrieNode const *node = root_;
    for (char ch : str) {
        node = step_(node, ch);
        if (node->term) {
            return true;
        }
    }
    return node->term;
}
