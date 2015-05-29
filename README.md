Cleaning the text of profanity.
===============================

Clearing text or texts corpus in Russian of obscene vocabulary.

Can be used with any set of stopwords; words are matched by lemmatization and similarities analysis.

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

Or if you have issues with boost-python:
```
python3 setup.py install --with-python
```

For OS X and Homebrew users:
```boost``` package is not enough, you need

```
brew install boost-python --with-python3
```

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
