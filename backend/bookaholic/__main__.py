from typing import List, Optional

import eel

from bookaholic.automatic_book import AutomaticBook
from bookaholic.book import Book
from bookaholic.library import Library


library = Library()

@eel.expose
def get_books() -> List[Book]:
    return library.get_books()

@eel.expose
def create_book_by_title_and_author_search(title: str, author: str) -> Optional[Book]:
    return AutomaticBook.new_from_title_and_author_search(title, author)

@eel.expose
def create_book_by_isbn_search(isbn: int) -> Optional[Book]:
    return AutomaticBook.new_from_isbn_search(isbn)

def add_book(book: Book):
    library.add_book(book)
    library.save()

def remove_book(book: Book):
    library.remove_book(book)
    library.save()