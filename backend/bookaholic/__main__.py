from typing import Any, Dict, List, Optional

import eel

from bookaholic.automatic_book import AutomaticBook
from bookaholic.book import Book
from bookaholic.book.rating.manager import RatingManager
from bookaholic.book.subject import FICTION_GENRES, NON_FICTION_GENRES
from bookaholic.library import Library


library = Library()
rating_manager = RatingManager(library)

@eel.expose
def get_library() -> Library._Data:
    """Return the entire library as a dictionary where ID is key and book is value"""
    return library.to_data()

@eel.expose
def get_fiction_genres() -> List[str]:
    """Return a list of all possible fiction genres"""
    return list(FICTION_GENRES.keys())

@eel.expose
def get_non_fiction_genres() -> List[str]:
    """Return a list of all possible non-fiction genres"""
    return list(NON_FICTION_GENRES.keys())

@eel.expose
def get_number_rated() -> int:
    return rating_manager.number_rated()

@eel.expose
def get_books_by_star(rating: int) -> List[int]:
    """Return a list of book ids where the book matches the rating"""
    return rating_manager.get_books_by_star(rating)

@eel.expose
def get_top_rated() -> List[int]:
    """Return a list of book ids where the book has 4 or more stars"""
    return rating_manager.get_top_rated()

@eel.expose
def get_rating_distribution() -> Dict[int, int]:
    return rating_manager.get_rating_distribution()

@eel.expose
def get_rating_summary() -> Dict[str, Any]:
    return rating_manager.generate_rating_summary()

@eel.expose
def create_book_by_title_and_author_search(title: str, author: str) -> Optional[Book._Data]:
    """Optionally return a new book created by title and author search (not yet present in library)"""
    return AutomaticBook.new_from_title_and_author_search(title, author).to_data()

@eel.expose
def create_book_by_isbn_search(isbn: int) -> Optional[Book._Data]:
    """Optionally return a new book created by ISBN search (not yet present in library)"""
    return AutomaticBook.new_from_isbn_search(isbn).to_data()

@eel.expose
def add_book(book: Book._Data) -> int:
    """Add a book to library, return book ID"""
    id_ = library.add_book(Book.from_data(book))
    library.save()

    return id_

@eel.expose
def finish_book(book_id: int, rating: int, finish_date: Optional[str]=None, review: Optional[str]="") -> Book._Data:
    """Mark a book as finished and assign it a rating (TO DO)"""
    return rating_manager.add_rating_from_book(
        book_id=book_id,
        rating=rating,
        finish_date=finish_date,
        review=review
    ).to_data()

@eel.expose
def remove_book(book_id: int):
    """Remove a book from library by ID"""
    library.remove_book(book_id)
    library.save()