/**
 * Corpus of texts
 */

// Copyright (c) Timur Iskhakov.
// Distributed under the terms of the MIT License.

#ifndef CORPUS_H
#define CORPUS_H

#ifdef BOOST_PYTHON
#include <boost/python.hpp>
#endif //BOOST_PYTHON

#include "str_set.hpp"

#include <exception>
#include <string>


class Corpus {
    /**
     * Input file path.
     */
    std::string input_path_;

    /**
     * Output destination.
     */
    std::string output_path_;

    /**
     * Set of stop words.
     */
    StrSet stop_set_;

    /**
     * I/O buffer size.
     */
    static size_t const BUFFER_SIZE;

    /**
     * Additional size for input buffer to store
     * proceeding sentence.
     */
    static size_t const MAX_SENTENCE_LENGTH;

    /**
     * Input file stream.
     */
    FILE *fin_;

    /**
     * Output file stream.
     */
    FILE *fout_;

    /**
     * Current input buffer size.
     */
    size_t buffer_loaded_size_;

    /**
     * Position in the output buffer, all the text before it
     * needs to be printed.
     */
    size_t output_buffer_pos_;

    /**
     * Proceeded input file size.
     */
    size_t proceed_size_;

    /**
     * Position in input buffer, all the text before it
     * is proceeded.
     */
    size_t last_write_pos_;

    /**
     * Input file size.
     */
    size_t input_file_size_;

    /**
     * Loaded input file size.
     */
    size_t input_loaded_size_;

    /**
     * Current position in input buffer.
     */
    size_t pos_;

    /**
     * Input buffer.
     */
    unsigned char input_buffer_[1024 * 1024 + 32 * 1024];

    /**
     * Output buffer.
     */
    unsigned char output_buffer_[1024 * 1024];

#ifdef BOOST_PYTHON

    /**
     * UIProgressBar.
     */
    boost::python::object progress_bar_;

#endif //BOOST_PYTHON

    /**
     * Establishes whether input is empty.
     */
    bool input_eof_() const;

    /**
     * Read input to newline character (or the file end).
     */
    void pick_eol_();

    /**
     * Get next symbol from input.
     */
    unsigned char get_next_symbol_();

    /**
     * Flush output buffer to file.
     */
    void flush_output_();

    /**
     * Write proceeding input buffer part to output buffer.
     */
    void write_buffer_();

    /**
     * Pass proceeding input buffer part.
     */
    void pass_buffer_();

    /**
     * Load more text from input stream to input buffer.
     */
    void load_buffer_();

    /**
     * Proceed a word in buffer.
     *
     * @return Current word
     */
    std::string proceed_word_();

    /**
     * Proceed a sentence.
     *
     * @return true if sentence doesn't contain obscene vocabulary
     */
    bool proceed_sentence_();

    /**
     * Proceed a xml file.
     */
    void proceed_xml_();

public:

#ifdef BOOST_PYTHON

    /**
     * A constructor.
     *
     * @param input_path Input file path
     * @param output_path Output destination
     * @param stop_list Line containing stop words
     * @param progress_bar UIProgressBar
     */
    Corpus(std::string const &input_path,
           std::string const &output_path,
           std::string const &stop_list,
           boost::python::object progress_bar) :
            input_path_(input_path),
            output_path_(output_path),
            stop_set_(stop_list),
            progress_bar_(progress_bar)
    { }

#else //BOOST_PYTHON

    /**
     * A constructor.
     *
     * @param input_path Input file path
     * @param output_path Output destination
     * @param stop_list Line containing stop words
     */
    Corpus(std::string const &input_path,
           std::string const &output_path,
           std::string const &stop_list) :
            input_path_(input_path),
            output_path_(output_path),
            stop_set_(stop_list),
    { }

#endif //BOOST_PYTHON

    /**
     * Proceed the corpus.
     */
    void proceed();
};

/**
 * Corpus exception.
 */
class CorpusException : std::exception {
    std::string message_;

public:
    CorpusException(char const *message) : message_(message) {}

    virtual char const * what() const throw() {
        return message_.c_str();
    }
};

#endif //CORPUS_H
