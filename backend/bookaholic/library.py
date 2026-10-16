from typing import List

import json
import os

from bookaholic.book import Book


ROOT = os.path.expanduser(r"~\.bookaholic")
DATA_PATH = os.path.join(ROOT, "books.json")

class Library:
    def __init__(self):
        # Make root if it does not already exist
        os.makedirs(ROOT, exist_ok=True)

        self._books = []

        if os.path.exists(DATA_PATH):

            with open(DATA_PATH, "r") as f:
                data = f.read()

            if data:
                self._books = [Book.from_data(b) for b in json.loads(data)]
            

    def get_books(self) -> List[Book]:
        return self._books.copy()

    def add_book(self, book: Book):
        self._books.append(book)

    def remove_book(self, book: Book):
        self._books.remove(book)

    def save(self):
        with open(DATA_PATH, "w") as f:
            json.dump([b.to_data() for b in self._books], f)