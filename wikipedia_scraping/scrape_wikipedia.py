from typing import Set
from urllib.request import HTTPError, urlopen
from bs4 import BeautifulSoup
import requests
import re
import os

# The number of related pages to get from our foundational pages above
NUM_RELATED_PAGES = 5

# The api url for wikipedia
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

# Where to get the foundational wikipedia pages
INPUT_FILE_NAME = 'input_pages.txt'

# What to name the output file
OUTPUT_FILE_NAME = 'scrape_output.txt'

# File path
ABS_PATH = f"{os.getcwd()}/"


# Script to read foundational wikipedia pages from file of name INPUT_FILE_NAME
def get_foundation_pages() -> Set[str]:
    # Create our output set
    foundation_pages = set()
    # Open the input file
    with open(f"{ABS_PATH}/{INPUT_FILE_NAME}", 'r') as f:
        # Read each line, take off the newline character, and place it in our set
        line = f.readline().strip()
        while line:
            foundation_pages.add(line)
            line = f.readline().strip()
    
    return foundation_pages


# Method to get NUM_RELATED_PAGES related pages for each page included in
# the foundational pages_to_scrape list above
def get_related_pages(page_title):
    # Request params
    params = {
        "action": "query",
        "prop": "links",
        "format": "json",
        "pllimit": NUM_RELATED_PAGES,
        "titles": page_title,
    }
    # Our response
    response = requests.get(WIKIPEDIA_API_URL, params=params)
    # extract the json form our response
    data = response.json()
    # Get the page_id from the original page we queried
    page_id = next(iter(data['query']['pages']))
    # Get the links
    links = data['query']['pages'][page_id].get('links', [])
    # Clean the links up a bit and return them
    return [link['title'].replace(' ', '_') for link in links]


# Function to scrape wikipedia
def scrape_website(page:str) -> str:
    # Specify the URL of the webpage
    source = urlopen(f'https://en.wikipedia.org/wiki/{page}')
    
    # Make a soup
    soup = BeautifulSoup(source, 'lxml')
    
    # See all the different unique tags
    #element_tags = set([text.parent.name for text in soup.find_all(string=True)])
   
    # Pull the text
    text = ''
    for paragraph in soup.find_all('p'):
        text += paragraph.text
    
    # Clean the text
    text = re.sub(r'\[.*?\]+', '', text)
    #text = text.replace('\n', ' ')
    
    return text


if __name__ == "__main__":

    # First delete any existing output file
    try:
        os.remove(f"{ABS_PATH}/{OUTPUT_FILE_NAME}")
        print("Deleted already existing output file.\n")
    except FileNotFoundError:
        print("Output file doesn't exist, skipping deletion.\n")

    # Get foundational pages from INPUT_FILE_NAME, returns a set
    pages_to_scrape = get_foundation_pages()

    # Find all related pages and expand our initial set
    for page in list(pages_to_scrape): # convert to list here as we cant iterate over a changing set
            print(f"Getting related pages for {page}")
            related_pages = get_related_pages(page)
            pages_to_scrape.update(related_pages)
            related_output = ", ".join(related_pages)
            print(f"Found {related_output}\n")

    print("\nFinished getting related pages, now performing scraping...\n")

    # Get how many pages we're scraping
    NO_PAGES_TO_SCRAPE = len(pages_to_scrape) # purely for letting the user know progress

    # Open the output file
    with open(f"output/{OUTPUT_FILE_NAME}", "a") as f:
        # List to keep track of the number of errors, and which pages caused them
        errors = [0]
        # i is to keep track of which page we're on to display progress
        i = 1
        # iterate over our set
        for page in pages_to_scrape:
            # try here as a bunch could go wrong
            try:
                # Scrape the page, and throw the result into our file
                f.write(scrape_website(page))
                # Alert the user of the scrape, and our progress
                print(f"Scraped and cleaned {page} ({(i/NO_PAGES_TO_SCRAPE) * 100:.0f}%)")
            except HTTPError: # If the page doesn't exist
                print(f"Couldn't get URL for https://en.wikipedia.org/wiki/{page}... Skipping...")
                errors[0] += 1
                errors.append(page)
            except UnicodeEncodeError: # If there's a unicode error
                print(f"Unicode error from {page}... Skipping...")
                errors[0] += 1
                errors.append(page)
            except Exception as e: # This is not good
                print(f"Error: {str(e)}")
                errors[0] += 1
                errors.append(page)
            i += 1

        # Report finish status
        print(f"\nFinished scraping {NO_PAGES_TO_SCRAPE} pages with {errors[0]} {'error' if errors[0] == 1 else 'errors'}!")
        # Output errors if we have any
        if errors[0] > 0:
            output_errors = '\n'.join(errors[1:])
            print(f"\nPages with errors:\n{output_errors}")
