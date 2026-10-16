from typing import Any, Callable, Dict, Optional

import json

import requests

from bookaholic import _string_utils
from bookaholic.book import Book
from bookaholic.book.metadata import Metadata
from bookaholic.book.status import Status
from bookaholic.book.subject import Subject


class AutomaticBook(Book):
    _Fields = Dict[str, Any]
    _Result = Dict[str, Any]

    def __new__(cls, fields: _Fields, filter: Callable[[_Fields, _Result], bool]) -> Optional[Book]:
        params = {
            "q":"language:eng",
            "fields": "key,title,subtitle,author_name,number_of_pages_median,editions,editions.cover_i,subject",
            **fields
        }

        response = requests.get("https://openlibrary.org/search.json", params=params)
        data = json.loads(response.text)

        # Filter books to those requested by user
        books = [b for b in data["docs"] if filter(fields, b)]

        if not books:
            return None
        
        # Find book title
        book = books[0]
        title = book["title"]
        subtitle = book.get("subtitle", False)

        if subtitle:
            title += ": " + subtitle

        # Find book author
        authors = [a for b in books for a in b["author_name"]]
        author = max(set(authors), key=authors.count)

        # Find number of pages
        n_pages = next((n for b in books if (n := b.get("number_of_pages_median", False))), 0)

        # Find cover URL
        cover_id = next((i for b in books for d in b["editions"]["docs"] if (i := d.get("cover_i", False))), None)
        cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg" if cover_id is not None else None

        metadata = Metadata(
            title=title,
            author=author,
            n_pages=n_pages,
            cover_url=cover_url
        )

        # Amalgamate subjects
        subjects = list(set([s for b in books for s in b.get("subject", [])]))
        subject = Subject.new_from_open_library(subjects)

        return Book(metadata, subject, Status.new_status())

    @classmethod
    def new_from_title_and_author_search(cls, title: str, author: str) -> Book:
        fields = {
            "title": title,
            "author": author
        }
        
        def filter(fields: AutomaticBook._Fields, results: AutomaticBook._Result) -> bool:
            title_is_match = _string_utils.compare(fields["title"], results["title"])
            author_is_match = any((_string_utils.compare(fields["author"], a) for a in results["author_name"]))
            
            return title_is_match and author_is_match
        
        return cls(fields, filter)

    @classmethod
    def new_from_isbn_search(cls, isbn: int) -> Book:
        fields = {"isbn": isbn}
        filter = lambda *_: True

        return cls(fields, filter)