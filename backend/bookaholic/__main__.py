from typing import Optional

import eel

from bookaholic.automatic_book import AutomaticBook
from bookaholic.book import Book
from bookaholic.library import Library


library = Library()

@eel.expose
def get_library() -> Library._Data:
    """Return the entire library as a dictionary where ID is key and book is value"""
    return library.to_data()

@eel.expose
def create_book_by_title_and_author_search(title: str, author: str) -> Optional[Book._Data]:
    """Optionally return a new book created by title and author search (not yet present in library)"""
    return AutomaticBook.new_from_title_and_author_search(title, author).to_data()

@eel.expose
def create_book_by_isbn_search(isbn: int) -> Optional[Book._Data]:
    """Pptionally return a new book created by ISBN search (not yet present in library)"""
    return AutomaticBook.new_from_isbn_search(isbn).to_data()

@eel.expose
def add_book(book: Book._Data) -> int:
    """Add a book to library, return book ID"""
    id_ = library.add_book(Book.from_data(book))
    library.save()

    return id_

@eel.expose
def remove_book(book_id: int):
    """Remove a book from library by ID"""
    library.remove_book(book_id)
    library.save()