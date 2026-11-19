from typing import Optional

from bookaholic._data import Data
from bookaholic.book.metadata import Metadata
from bookaholic.book.rating import Rating
from bookaholic.book.subject import Subject


class Book(Data):
    def __init__(self, metadata: Metadata, subject: Subject, rating: Optional[Rating]=None):
        self["metadata"] = metadata
        self["subject"] = subject
        self["rating"] = rating
    
    @classmethod
    def from_data(cls, data: Book._Data) -> Book:
        metadata = Metadata.from_data(data["metadata"])
        subject = Subject.from_data(data["subject"])
        rating = Rating.from_data(data["rating"]) if data["rating"] else None

        return cls(metadata, subject, rating)

    @property
    def days_spent(self) -> Optional[int]:
        """Total days taken to read (minimum 1 day)."""
        if self["rating"]:
            delta = (self["rating"]["finish_date"] - self["metadata"]["start_date"]).days
            return max(1, delta + 1)
        
        return None

    @property
    def reading_speed(self) -> float:
        """Pages read per day for this book."""
        if self.days_spent:
            return round(self["metadata"]["n_pages"] / self.days_spent, 2)
        return 0

    def to_data(self) -> Book._Data:
        data = {}

        data["metadata"] = self["metadata"].to_data()
        data["rating"] = self["rating"].to_data() if self["rating"] else None
        data["subject"] = self["subject"].to_data()

        return data