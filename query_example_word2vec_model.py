from gensim.models import Word2Vec
import os

# name of the model we're using
MODEL = 'example_model'

if __name__ == '__main__':
    # Get the absolute path
    abspath = os.path.dirname(os.path.abspath(__file__))
    # Load the model
    model = Word2Vec.load(os.path.join(abspath, f"word2vec/saved_models/{MODEL}"))

    # Display total vocab
    print(f"Total vocabulary: {len(model.wv.key_to_index)}")

    # Test the relationships
    test_word = input("\nTest Word: ")
    while test_word != "":
        try:
            print(f"Most similar to {model.wv.most_similar(positive=test_word)}")
        except:
            print(f"Couldn't find {test_word}!")
        
        test_word = input("\nTest Word: ")
