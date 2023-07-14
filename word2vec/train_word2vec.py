import gensim
from typing import Iterator, List
import os

# Absolute path
ABSOLUTE_PATH = f"{os.getcwd()}/"

# The location of our training data RELATIVE to this python file
TRAINING_DATA = "../wikipedia_scraping/output_data/example_scrape_output.txt"

# Method to read in our training data
def read_input(input_file:str) -> Iterator[List[str]]:
    with open(input_file, 'r') as f: # do gzip.open for gzipped files
        for i, line in enumerate(f):
            # do some pre-processing and return list of words for each review
            # text
            if (i % 1000 == 0):
                print(f"Processed {i} lines")

            tokenized_line = gensim.utils.simple_preprocess(line)
            yield tokenized_line


if __name__ == '__main__':

    # Get the full path of our training data file
    data_file = os.path.join(ABSOLUTE_PATH, TRAINING_DATA)

    # Get our tokenized input into a list
    # Every line has become a list of words
    # So this is a two dimensional matrix
    documents = list(read_input(data_file))


    print("Building vocabulary in Word2Vec model...")
    
    # Build the model's vocabulary
    model = gensim.models.Word2Vec(
        documents,
        vector_size=125,
        window=10,
        min_count=2,
        workers=10)

    print("Training Word2Vec model...")
    # Train the model
    model.train(documents, total_examples=len(documents), epochs=15)

    # Save the model
    model.save(os.path.join(ABSOLUTE_PATH, "saved_models/my_model"))

    # Save the vectors
    model.wv.save(os.path.join(ABSOLUTE_PATH, "saved_vectors/my_vectors"))

    # Report that we've finished training
    print("\n FINISHED TRAINING! \n")
    print(f"Model's total vocabulary: {len(model.wv.key_to_index)}")
