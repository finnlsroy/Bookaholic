from typing import Optional

from datetime import datetime

from bookaholic._string_utils import capitalize
from bookaholic._data import Data


class Metadata(Data):
    def __init__(
        self,
        title: str,
        author: str,
        n_pages: int,
        cover_url: Optional[str]=None,
        start_date: Optional[str]=None
    ):
        self["title"] = capitalize(title)
        self["author"] = capitalize(author)
        self["n_pages"] = n_pages
        self["cover_url"] = cover_url

        # Default to today if start_date is not provided
        if start_date:
            self["start_date"] = datetime.strptime(start_date, "%Y-%m-%d").date()
        else:
            self["start_date"] = datetime.now().date()