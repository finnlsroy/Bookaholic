"""
Book Rating Module for Bookaholic (Dev 2.0)
Allows rating books from 1 to 5 stars upon completion.
Matches variables used by teammates (n_pages, title, author) and reading stats.
"""
from typing import Optional

from datetime import datetime

from bookaholic._data import Data


class Rating(Data):
    """Stores rating details for a finished book."""
    def __init__(
        self,
        rating: int,
        finish_date: Optional[str]=None,
        review: Optional[str]=""
    ):
        self["rating"] = self._validate_rating(rating)
        
        # Default to today if finish_date is not provided
        if finish_date:
            self["finish_date"] = datetime.strptime(finish_date, "%Y-%m-%d").date()
        else:
            self["finish_date"] = datetime.now().date()
            
        self["review"] = review

    def _validate_rating(self, rating: int) -> int:
        """Ensures rating is an integer between 1 and 5 stars."""
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5 stars.")
        return rating

'''
# Quick test execution
if __name__ == "__main__":
    manager = RatingManager()

    # Testing with variables matching teammate's Book class (n_pages, title, author)
    manager.add_rating(
        title="Cien Años De Soledad",
        author="Gabriel García Márquez",
        n_pages=417,
        rating=5,
        finish_date="2026-01-15",
        review="Amazing masterpiece!"
    )

    manager.add_rating(
        title="El Principito",
        author="Antoine De Saint-Exupéry",
        n_pages=96,
        rating=4,
        finish_date="2026-02-03",
        review="Short and inspiring."
    )

    summary = manager.generate_rating_summary()
    print("--- RATING SYSTEM SUMMARY ---")
    print(f"Total Rated Books: {summary['total_rated_books']}")
    print(f"Average Rating: {summary['average_rating']} / 5.0")
    print(f"Star Distribution: {summary['star_distribution']}")
'''