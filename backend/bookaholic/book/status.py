from typing import Optional

from datetime import date, datetime

from bookaholic._data import Data


class Status(Data):
    def __init__(self, start_date: date, end_date: Optional[date]):
        self["start_date"] = start_date
        self["end_date"] = end_date

    @classmethod
    def new_status(cls) -> Status:
        return cls(datetime.now().date(), None)

    @classmethod
    def from_data(cls, data: Status._Data) -> Status:
        start_date = date.fromisoformat(data["start_date"])

        end_date = data["start_date"]
        end_date = None if end_date is None else date.fromisoformat(end_date)
        
        return cls(start_date, end_date)

    def finish_book(self, end_date: str):
        self["end_date"] = date.fromisoformat(end_date)

    def to_data(self) -> Status._Data:
        data = dict()

        data["start_date"] = str(self["start_date"])

        end_date = self["end_date"]
        data["end_date"] = None if end_date is None else str(end_date)
        
        return data