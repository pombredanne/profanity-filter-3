"""
Project metadata
Information describing the project.
"""

# Copyright (c) Timur Iskhakov.
# Distributed under the terms of the MIT License.


package = 'profanity_filter'
project = "profanity-filter"
version = '0.4'
description = 'Cleaning the text of profanity.'
long_description = '''\
Clearing text or texts corpus in Russian of obscene vocabulary.\n
Can be used with any set of stopwords; words are matched by \
lemmatisation (using pymorphy2) and similarities analysis.'''
authors = ['Timur Iskhakov']
authors_string = ', '.join(authors)
emails = ['iskhakovt@gmail.com']
license = 'MIT'
copyright = '2015 ' + authors_string
url = 'https://github.com/cs-hse-projects/profanity-filter/'
