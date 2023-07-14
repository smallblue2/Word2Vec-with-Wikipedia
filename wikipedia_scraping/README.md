# Wikipedia Scraping
The python file `wikipedia_scraping.py` reads in user-defined pages from `input_pages.txt`, finds additional related pages, and scrapes and cleans all pages.

The purpose of this is to gather training data for the Word2Vec model for whatever your specific usecase may be, specifying where you want your training data to come from allows you to ensure the context that Word2Vec will train on.

# input_pages.txt
This is a list of pages in the form of postfixes to the url `https://en.wikipedia.org/wiki/`.

For example, if I want to scrape `https://en.wikipedia.org/wiki/Eric_Idle`, I would include `Eric_Idle` in the file.

The python script will then continue to find up to 5 related pages on `Eric_Idle`, and scrape them too!

# Output
The output of the file is a giant `.txt` file, by default placed within `output_data/`.

This is training data for the Word2Vec model inside `../Word2Vec/`.
