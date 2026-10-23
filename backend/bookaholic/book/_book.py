from typing import Any, Dict

from bookaholic._data import Data
from bookaholic.book.metadata import Metadata
from bookaholic.book.status import Status
from bookaholic.book.subject import Subject


class Book(Data):
    def __init__(self, metadata: Metadata, subject: Subject, status: Status):
        self["metadata"] = metadata
        self["subject"] = subject
        self["status"] = status
    
    @classmethod
    def from_data(cls, data: Book._Data) -> Book:
        metadata = Metadata.from_data(data["metadata"])
        subject = Subject.from_data(data["subject"])
        status = Status.from_data(data["status"])

        return cls(metadata, subject, status)

    def to_data(self) -> Book._Data:
        data = {}

        data["metadata"] = self["metadata"].to_data()
        data["subject"] = self["subject"].to_data()
        data["status"] = self["status"].to_data()

        return data