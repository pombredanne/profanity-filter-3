// Copyright (c) Timur Iskhakov.
// Distributed under the terms of the MIT License.


#include "corpus.hpp"

#include <cstdio>
#include <cstring>
#include <iostream>


size_t const Corpus::BUFFER_SIZE = 1024 * 1024;
size_t const Corpus::MAX_SENTENCE_LENGTH = 1024 * 1024;

bool Corpus::input_eof_() const {
    return input_file_size_ == input_loaded_size_ && pos_ == buffer_loaded_size_;
}

#ifdef STRICT_FILE

void Corpus::pick_eol_() {
    while (get_next_symbol_() != '\n');
}

#else //STRICT_FILE

void Corpus::pick_eol_() {
    unsigned char ch;
    do {
        ch = get_next_symbol_();
    } while (ch != '\n' && ch);
}

#endif //STRICT_FILE

unsigned char Corpus::get_next_symbol_() {
    if (input_eof_()) {
        return 0;
    }

    if (pos_ == buffer_loaded_size_) {
        load_buffer_();
    }

    return input_buffer_[pos_++];
}

void Corpus::flush_output_() {
    if (fwrite(output_buffer_, 1, output_buffer_pos_, fout_) != output_buffer_pos_) {
        throw CorpusException("Write error");
    }

#ifdef BOOST_PYTHON
    progress_bar_.attr("step")(proceed_size_);
#endif //BOOST_PYTHON

    output_buffer_pos_ = 0;
    proceed_size_ = 0;
}

void Corpus::write_buffer_() {
    if (pos_ - last_write_pos_ > BUFFER_SIZE - output_buffer_pos_) {
        flush_output_();
    }

    memcpy(output_buffer_ + output_buffer_pos_, input_buffer_ + last_write_pos_, pos_ - last_write_pos_);
    output_buffer_pos_ += pos_ - last_write_pos_;
    pass_buffer_();
}

void Corpus::pass_buffer_() {
    proceed_size_ += pos_ - last_write_pos_;
    last_write_pos_ = pos_;
}

void Corpus::load_buffer_() {
    if (pos_ - last_write_pos_ > MAX_SENTENCE_LENGTH) {
        throw CorpusException("Too long sentence");
    }

    for (size_t i = last_write_pos_; i != buffer_loaded_size_; ++i) {
        input_buffer_[i - last_write_pos_] = input_buffer_[i];
    }

    pos_ = buffer_loaded_size_ - last_write_pos_;
    last_write_pos_ = 0;
    size_t read_size = fread(input_buffer_ + pos_, 1, BUFFER_SIZE, fin_);
    buffer_loaded_size_ = pos_ + read_size;
    input_loaded_size_ += read_size;

    if (read_size != BUFFER_SIZE && input_loaded_size_ != input_file_size_) {
        throw CorpusException("Read error");
    }
}

std::string Corpus::proceed_word_() {

#ifdef STRICT_FILE

    size_t hyphen_pos = pos_;
    while (input_buffer_[--hyphen_pos] != '-');
    size_t sep_pos = hyphen_pos;
    while (input_buffer_[--sep_pos] != '\t');

#else //STRICT_FILE

    size_t hyphen_pos = pos_ - 1;
    while (hyphen_pos >= last_write_pos_ && input_buffer_[hyphen_pos] != '-') {
        --hyphen_pos;
    }
    size_t sep_pos = hyphen_pos - 1;
    while (sep_pos >= last_write_pos_ &&
           input_buffer_[sep_pos] != ' ' &&
           input_buffer_[sep_pos] != '\t')
    {
        --sep_pos;
    }

    if (sep_pos < last_write_pos_) {
        throw CorpusException("Corpus is broken");
    }

#endif //STRICT_FILE

    input_buffer_[hyphen_pos] = 0;
    std::string word(reinterpret_cast<char *>(input_buffer_ + sep_pos + 1));
    input_buffer_[hyphen_pos] = '-';
    return word;
}

bool Corpus::proceed_sentence_() {
    std::vector<std::string> words;

    while (!input_eof_()) {
        unsigned char first = get_next_symbol_();

        // Cyrillic letter UTF-8
        if (first == 208 || first == 209) {
            pick_eol_();
            words.push_back(proceed_word_());
        } else if (first == '<' &&
                   get_next_symbol_() == '/' &&
                   get_next_symbol_() == 's' &&
                   get_next_symbol_() == '>')
        {
            pick_eol_();
            return !stop_set_.check_occurrence(words);
        } else {
            pick_eol_();
        }
    }

    throw CorpusException("Corpus is broken");
}

void Corpus::proceed_xml_() {
    while (!input_eof_()) {
        if (get_next_symbol_() == '<' &&
            get_next_symbol_() == 's' &&
            get_next_symbol_() == '>')
        {
            pick_eol_();
            if (proceed_sentence_()) {
                write_buffer_();
            } else {
                pass_buffer_();
            }
        } else  {
            pick_eol_();
            write_buffer_();
        }
    }
}

void Corpus::proceed() {
    if (stop_set_.empty()) {
        std::cout << "Stoplist is empty!\n";
    }

    fin_ = fopen(input_path_.c_str(), "rb");
    fout_ = fopen(output_path_.c_str(), "wb");

    if (ferror(fin_)) {
        throw CorpusException("Failed to open input file");
    }
    if (ferror(fout_)) {
        throw CorpusException("Failed to open output file");
    }

    fseek(fin_, 0L, SEEK_END);
    input_file_size_ = static_cast<size_t>(ftell(fin_));
    fseek(fin_, 0L, 0);

#ifdef BOOST_PYTHON
    progress_bar_.attr("init")(input_file_size_);
#endif //BOOST_PYTHON

    proceed_xml_();
    flush_output_();

    fclose(fin_);
    fclose(fout_);
}
