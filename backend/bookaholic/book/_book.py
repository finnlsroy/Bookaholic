from typing import Any, Dict

from bookaholic.book.metadata import Metadata
from bookaholic.book.status import Status
from bookaholic.book.subject import Subject


class Book(dict):
    _Data = Dict[str, Any]

    def __init__(self, metadata: Metadata, subject: Subject, status: Status):
        self["metadata"] = metadata
        self["subject"] = subject
        self["status"] = status
    
    @classmethod
    def from_data(cls, data: _Data) -> Book:
        metadata = Metadata.from_data(data["metadata"])
        subject = Subject.from_data(data["subject"])
        status = Status.from_data(data["status"])

        return cls(metadata, subject, status)

    def to_data(self) -> _Data:
        data = {}

        data["metadata"] = self["metadata"].to_data()
        data["subject"] = self["subject"].to_data()
        data["status"] = self["status"].to_data()

        return data