from typing import List, Dict, Any, Optional

from bookaholic.book import Book
from bookaholic.book.rating import Rating
from bookaholic.library import Library


class RatingManager:
    """Manages book ratings, calculations, and filtering."""
    def __init__(self, library: Library):
        self._library = library

    def add_rating_from_book(self, book_id: int, rating: int, finish_date: Optional[str]=None, review: Optional[str]="") -> Book:
        """Helper to create a rating directly from teammate's Book object/dict."""
        book = self._library[book_id]
        book["rating"] = Rating(
            rating=rating,
            finish_date=finish_date,
            review=review
        )

        self._library.save()
        
        return book

    def number_rated(self) -> int:
        return [b["rating"] is not None for b in self._library.values()].count(True)

    def average_rating(self) -> float:
        """Calculate overall average rating across all books."""
        if not len(self._library):
            return 0.0
        total_stars = sum([r["rating"] for b in self._library.values() if (r := b.get("rating", None)) ])
        return round(total_stars / self.number_rated(), 2)

    def get_books_by_star(self, stars: int) -> List[int]:
        """Filter books by exact star rating (1 to 5)."""
        return [i for i, b in self._library.items() if b["rating"] and b["rating"]["rating"] == stars]

    def get_top_rated(self, min_stars: int = 4) -> List[int]:
        """Get highly rated books (e.g. 4 or 5 stars)."""
        return [i for i, b in self._library.items() if b["rating"] and b["rating"]["rating"] >= min_stars]

    def get_rating_distribution(self) -> Dict[int, int]:
        """Count how many books received 1, 2, 3, 4, or 5 stars."""
        dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for b in self._library.values():
            rating = b.get("rating", None)

            if rating:
                dist[rating["rating"]] += 1
        
        return dist

    def generate_rating_summary(self) -> Dict[str, Any]:
        """Generate a complete summary report of ratings."""
        return {
            "total_rated_books": self.number_rated(),
            "average_rating": self.average_rating(),
            "star_distribution": self.get_rating_distribution(),
            "top_rated_count": len(self.get_top_rated())
        }