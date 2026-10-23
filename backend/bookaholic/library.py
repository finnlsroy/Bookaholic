from typing import Dict

import json
import os

from bookaholic.book import Book


ROOT = os.path.expanduser(r"~\.bookaholic")
DATA_PATH = os.path.join(ROOT, "books.json")

class Library(dict):
    _Data = Dict[str, Book._Data]

    def __init__(self, ):
        # Make root if it does not already exist
        os.makedirs(ROOT, exist_ok=True)

        if os.path.exists(DATA_PATH):

            with open(DATA_PATH, "r") as f:
                data = f.read()

            if data:
                books = [Book.from_data(b) for b in json.loads(data)]

                for book in books:
                    self[id(book)] = book

    def add_book(self, book: Book) -> int:
        id_ = id(book)
        self[id_] = book

        return id_

    def remove_book(self, book_id: int):
        del self[book_id]

    def to_data(self) -> _Data:
        return {i: b.to_data() for i, b in self.items()}

    def save(self):
        with open(DATA_PATH, "w") as f:
            json.dump([b.to_data() for b in self.values()], f)