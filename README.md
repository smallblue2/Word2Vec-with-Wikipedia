# Word2Vec-with-Wikipedia
An intuitive way to build a vector space of vocabulary with Word2Vec from contexts derived from Wikipedia through webscraping.

This repository sets you up to easily and quickly train a Word2Vec model on easily accessible training data from scraping Wikipedia.

## Scraping Wikipedia
All files for scraping wikipedia is included in `./wikipedia_scraping/`.

The method that I implemented allows you to **specify foundational pages in wikipedia**. \
It will then branch out and access **five related pages per foundational page** - of which is easily configurable from 5 within the script.

This is to allow the user to essentially specify a context area that they can build their vector space from, with the example provided being around the topic of Health, Science and Education.

All gathered pages are then scraped and cleaned for training data and saved to a text file, ready for the word2vec model to be trained on.

## Word2Vec
All files for Word2Vec are contained within `./word2vec/`.

The included script uses python's gensim's implementation of Word2Vec, which is essentially a direct implementation of Google's original model, with more bells and springs added.

The script will train the Word2Vec model on the data gathered from scraping Wikipedia, and will by default save it's model and word vectors to `./word2vec/saved_models/` and `./word2vec/saved_vectors/` respectively.

## Demo
This repository contains an already pre-trained Word2Vec model, trained from data scraped from wikipedia from pages specified in the `wikipedia_scraping/input_pages.txt`.

Simply clone the repository and run `python3 query_example_word2vec_model.py` to query it's vector space/vocabulary.
