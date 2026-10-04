from typing import Any, Callable, Dict, Optional, Self, Set

import json
import re
import string

import requests
from num2words import num2words


IRRELEVANT_WORDS = ["a", "an", "and", "of", "the", "to"]

class Book(dict):
    _Fields = Dict[str, Any]
    _OpenLibraryBook = Dict[str, Any]

    def __init__(self, title: str, author: str, n_pages: int, cover_id: int):
        self["title"] = string.capwords(title)
        self["author"] = string.capwords(author)
        self["n_pages"] = n_pages

        # Different sizes of cover
        url_base = f"https://covers.openlibrary.org/b/id/{cover_id}-%s.jpg"

        self["cover_small"] = url_base % "S"
        self["cover_medium"] = url_base % "M"
        self["cover_large"] = url_base % "L"

    @classmethod
    def _new_from_open_library(cls, fields: _Fields, filter: Callable[[_Fields, _OpenLibraryBook], bool]) -> Optional[Self]:
        title = None
        author = None
        n_pages = None
        cover_id = None
        
        params = {
            "q":"language:eng",
            "fields": "key,title,author_name,number_of_pages_median,editions,editions.cover_i",
            **fields
        }

        response = requests.get("https://openlibrary.org/search.json", params=params)
        data = json.loads(response.text)

        # For debugging purposes
        #print(data["num_found"], "matching books found")

        for book in data["docs"]:

            if filter(fields, book):

                if title is None:
                    title = string.capwords(book["title"])

                if author is None:
                    author = string.capwords(", ".join(book["author_name"]))

                if n_pages is None:
                    n_pages = book.get("number_of_pages_median", None)

                if cover_id is None:
                    editions = book["editions"]["docs"]
                
                    if editions:
                        cover_id = editions[0].get("cover_i", None)

                if title and author and n_pages and cover_id:
                    return cls(title, author, n_pages, cover_id)

        return None

    @classmethod
    def new_from_title_and_author(cls, title: str, author: str) -> Optional[Self]:
        # Convert a book or author name to a set of comparable keywords
        def string_to_keywords(string: str) -> Set[str]:
            # Replace numbers with words
            words = re.split(r"\S+", string)
            words = [c if not c.isnumeric() else num2words(c) for c in words]
            string = " ".join(words)

            # Convert to lowercase
            string = string.lower()
            # Replace hyphens with spaces
            string = string.replace("-", " ")
            # Remove characters that are not alphanumeric or whitespace
            string = re.sub(r"[^a-z\s]", "", string)
    
            # Remove irrelevant words (ex. "the")
            keywords = re.split(r"[\s-]", string)
            keywords = [k for k in keywords if not k in IRRELEVANT_WORDS]
    
            return set(keywords)

        # Compare strings to determine whether one is a subset of the other
        def compare_strings(a: str, b: str) -> bool:
            a_keywords = string_to_keywords(a)
            b_keywords = string_to_keywords(b)
    
            return a_keywords.issubset(b_keywords) or b_keywords.issubset(a_keywords)

        fields = {
            "title": title,
            "author": author
        }
        
        def filter(fields: Book._Fields, book: Book._OpenLibraryBook) -> bool:
            title_is_match = compare_strings(fields["title"], book["title"])
            author_is_match = any((compare_strings(fields["author"], a) for a in book["author_name"]))
            
            return title_is_match and author_is_match

        return cls._new_from_open_library(fields, filter)

    @classmethod
    def new_from_isbn(cls, isbn: int) -> Optional[Self]:
        fields = {"isbn": isbn}
        filter = lambda *_: True # Don't filter the results

        return cls._new_from_open_library(fields, filter)

if __name__ == "__main__":
    book = Book.new_from_title_and_author(input("Title >>> "), input("Author >>> "))
    #book = Book.new_from_isbn(int(input("ISBN >>> ")))

    if not book is None:
        print(book["title"], "by", book["author"])
        print(book["n_pages"], "pages long")
        print(book["cover_large"])
    else:
        print("Book not found")