from typing import Optional

import json
import re

import requests
from num2words import num2words


def clean_name(name: str) -> str:
    # Replace numbers with words
    chunks = re.split(r"\\s+", name)
    chunks = [c if not c.isnumeric() else num2words(c) for c in chunks]
    name = " ".join(chunks)

    # Remove irrelevant words
    chunks = re.split(r"[\\s-]", name.lower())
    chunks = [c for c in chunks if not c in ["the", "and", "of"]]
    name = "".join(chunks)

    # Make lower-case, no spaces
    return re.sub(r"[^a-z]", "", name)

def get_book_id(title: str, author: str) -> Optional[str]:
    params = {
        "title": title,
        "author": author,
        "fields": "title,author_name,edition_key"
    }

    response = requests.get("https://openlibrary.org/search.json", params=params)
    data = json.loads(response.text)

    for doc in data["docs"]:
        print(doc)
        if clean_name(title) in clean_name(doc["title"]):

            author_clean = clean_name(author)

            for doc_author in doc["author_name"]:

                if author_clean in clean_name(doc_author):
                    
                    return max(doc["edition_key"], key=(lambda k: int(k[2:-1])))

if __name__ == "__main__":
    title = input("Title >>> ")
    author = input("Author >>> ")

    book_id = get_book_id(title, author)

    if book_id is not None:
        print(f"https://covers.openlibrary.org/b/olid/{book_id}-M.jpg")
    else:
        print("Could not find cover.")