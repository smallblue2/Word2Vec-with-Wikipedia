# Word2Vec
Word2Vec is a model that maps words to high dimensional vector spaces through the context of their use in training data.

This directory simply provides a script to train a Word2Vec model, based on training data gathered from performing webscraping in `../wikipedia_scraping/`.

# Training the Model
Simply run `python3 train_word2vec.py`, ensuring you have generated training data with `../wikipedia_scraping`, and you will get a model outputted within `./saved_models/` named `my_model`. 

Additionally, the word vectors will also be saved within `./saved_vectors/`.

# Using the Model
Once you have trained your model, you can easily load it using the gensim python library. \
See `../query_example_word2vec_model.py`.
