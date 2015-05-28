// Copyright (c) Timur Iskhakov.
// Distributed under the terms of the MIT License.


#include "aho_corasick.hpp"


AhoCorasick::AhoCorasick(std::vector<std::string> const &patterns) {
    for (auto const &pattern : patterns) {
        add_pattern_(" " + pattern + " ");
    }

}

void AhoCorasick::add_pattern_(std::string const &pattern) {

}

void AhoCorasick::proceed_aho_corasick_() {

}

bool AhoCorasick::occurre(std::string const &str) const {
    return false;
}
