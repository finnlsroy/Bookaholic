from typing import Any, Dict, List, Optional

import json
import os
from collections import defaultdict

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

    def _finished_books(self) -> List[Book]:
        return [b for b in self.values() if b["rating"]]

    def add_book(self, book: Book) -> int:
        id_ = id(book)
        self[id_] = book

        return id_

    def remove_book(self, book_id: int):
        del self[book_id]

    def total_books_read(self) -> int:
        """Return total number of finished books."""
        return len(self._finished_books())

    def total_pages_read(self) -> int:
        """Return total pages read across all books."""
        return sum(b["metadata"]["n_pages"] for b in self._finished_books())

    def stats_by_year(self) -> Dict[int, Dict[str, int]]:
        """Get books and pages read per year."""
        stats = defaultdict(lambda: {"books": 0, "pages": 0})
        for book in self._finished_books():
            year = book["rating"]["finish_date"].year
            stats[year]["books"] += 1
            stats[year]["pages"] += book["metadata"]["n_pages"]
        return dict(stats)

    def stats_by_month(self, year: Optional[int] = None) -> Dict[str, Dict[str, int]]:
        """Get books and pages read per month (YYYY-MM)."""
        stats = defaultdict(lambda: {"books": 0, "pages": 0})
        for book in self._finished_books():
            if year is None or book["rating"]["finish_date"].year == year:
                key = book["rating"]["finish_date"].strftime("%Y-%m")
                stats[key]["books"] += 1
                stats[key]["pages"] += book["metadata"]["n_pages"]
        return dict(stats)

    def stats_by_week(self, year: Optional[int] = None) -> Dict[str, Dict[str, int]]:
        """Get books and pages read per week (YYYY-Www)."""
        stats = defaultdict(lambda: {"books": 0, "pages": 0})
        for book in self._finished_books():
            if year is None or book["rating"]["finish_date"].year == year:
                key = book["rating"]["finish_date"].strftime("%Y-W%U")
                stats[key]["books"] += 1
                stats[key]["pages"] += book["metadata"]["n_pages"]
        return dict(stats)

    def overall_daily_average(self) -> float:
        """Calculate overall average pages read per day."""
        finished = self._finished_books()

        if not len(finished):
            return 0.0
        
        min_date = min(log["metadata"]["start_date"] for log in finished)
        max_date = max(log["rating"]["finish_date"] for log in finished)
        total_days = max(1, (max_date - min_date).days + 1)
        return round(self.total_pages_read() / total_days, 2)

    def rank_books_by_speed(self, fastest_first: bool = True) -> List[int]:
        """Rank books by reading speed (pages / time taken)."""
        sorted_books = sorted(self._finished_books(), key=lambda b: b.reading_speed, reverse=fastest_first)
        return [id(b) for b in sorted_books]

    def generate_summary(self) -> Dict[str, Any]:
        """Generate full statistics summary dictionary."""
        return {
            "total_books": self.total_books_read(),
            "total_pages": self.total_pages_read(),
            "overall_daily_avg_pages": self.overall_daily_average(),
            "by_year": self.stats_by_year(),
            "by_month": self.stats_by_month(),
            "by_week": self.stats_by_week(),
            "speed_ranking": self.rank_books_by_speed(fastest_first=True)
        }

    def to_data(self) -> _Data:
        return {i: b.to_data() for i, b in self.items()}

    def save(self):
        with open(DATA_PATH, "w") as f:
            json.dump([b.to_data() for b in self.values()], f)