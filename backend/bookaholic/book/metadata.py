from typing import Optional

import string

from bookaholic.book._data import Data


class Metadata(Data):
    def __init__(self, title: str, author: str, n_pages: int, cover_url: Optional[str]=None):
        self["title"] = string.capwords(title)
        self["author"] = string.capwords(author)
        self["n_pages"] = n_pages
        self["cover_url"] = cover_url