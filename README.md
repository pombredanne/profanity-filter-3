Cleaning the text of profanity.
===============================

Clearing text or texts corpus in Russian of obscene vocabulary.

Can be used with any set of stopwords; words are matched by lemmatisation (using [pymorphy2](https://github.com/kmike/pymorphy2)) and similarities analysis.


---
### Requirements

  * Python 3.4+ **with headers**
  * C++ compiler
  * Boost with python3

### Installation

```bash
git clone https://github.com/cs-hse-projects/profanity-filter
cd profanity-filter
python3 setup.py install
```

##### Additional flags:
* `--with-boost` If you have issues with boost-python (sudo may be required).
* `--no-corpus-check` If you are sure that your corpus is well-formatted. See the description below.

For OS X and Homebrew users:
```boost``` package is not enough, you need

```
brew install boost-python --with-python3
```


---
### Usage
```
usage: profanity-filter [-h] [--type [{corpus,text}]] [--stoplist STOPLIST] input output

positional arguments:
  input                     Input file
  output                    Output destination

optional arguments:
  -h, --help                show help message and exit
  --type [{corpus,text}]    Input file type (vert is corpus by default)
  --stoplist STOPLIST       Custom stoplist file
```

**Only UTF-8 encoding is supported.**


---
### Corpus structure

To be written later.


---
### Texts similarities analysis

To be written later.


---
