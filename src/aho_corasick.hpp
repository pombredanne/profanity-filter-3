/**
 * Set of string with a quick check on the occurrence of a set of words
 * implemented via Aho-Corasick algorithm.
 */

// Copyright (c) Timur Iskhakov.
// Distributed under the terms of the MIT License.


#ifndef AHO_CORASICK_HPP
#define AHO_CORASICK_HPP

#include <map>
#include <string>
#include <vector>


class AhoCorasick {
    /**
     * Trie node with fail link.
     */
    struct TrieNode {
        /**
         * Common trie links.
         */
        std::map<char const, TrieNode *> links;

        /**
         * "Dictionary suffix" link.
         */
        TrieNode *fail;

        /**
         * Represents the end of a word.
         */
        bool term;

    public:
        /**
         * A constructor.
         *
         * @param fail_node Fail link
         */
        TrieNode(TrieNode *fail_node = nullptr) :
                fail(fail_node),
                term(false)
        { }

        /**
         * Get the common trie link by character.
         *
         * @param ch A character to follow
         * @return Link if exists else NULL
         */
        TrieNode * get_link(char ch) const {
            auto iter = links.find(ch);
            return (iter != links.cend() ? iter->second : nullptr);
        }
    };

    /*
     * The root of the trie.
     * fail is linked to NULL.
     */
    TrieNode *root_;

    /**
     * Recursively deletes a node and its children.
     *
     * @param node The node to delete
     */
    void delete_node_(TrieNode *);

    /**
     * Gets next node for a char in the trie.
     *
     * @param node Current node
     * @param ch The char to proceed
     * @return Next node
     */
    TrieNode const * step_(TrieNode const *, char) const;

public:
    /*
     * A constructor.
     */
    AhoCorasick() : root_(new TrieNode(nullptr)) {}

    /**
     * A destructor.
     */
    ~AhoCorasick();

    /**
     * Adds a pattern to the trie.
     *
     * @param pattern The pattern to add
     * @return Uniqueness of the pattern
     */
    bool add_pattern(std::string const &);

    /**
     * Initialises fail links via Aho-Corasick algorithm.
     */
    void proceed_aho_corasick();

    /**
     * Checks an occurrence of a substring of a string in the set.
     *
     * @param str String to find
     * @return True if a substring of str is in the set.
     */
    bool occur(std::string const &) const;
};

#endif //AHO_CORASICK_HPP
