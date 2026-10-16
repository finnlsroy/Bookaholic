from typing import Set

import re
from string import capwords

from num2words import num2words


IRRELEVANT_WORDS = ["a", "an", "and", "of", "the", "to"]


def capitalize(string: str) -> str:
    return capwords(string)

def compare(a: str, b: str) -> bool:
    # Convert string to a set of comparable keywords
    def string_to_keywords(string: str) -> Set[str]:
        # Replace numbers with words
        words = re.split(r"\s+", string)
        words = [c if not c.isnumeric() else num2words(c) for c in words]
        string = " ".join(words)
        
        # Convert to lowercase
        string = string.lower()
        # Replace hyphens (from numwords) with spaces
        string = string.replace("-", " ")
        # Remove characters that are not alphanumeric or whitespace
        string = re.sub(r"[^a-z\s]", "", string)
        
        # Remove irrelevant words (ex. "the")
        keywords = re.split(r"[\s-]", string)
        keywords = [k for k in keywords if not k in IRRELEVANT_WORDS]

        return set(keywords)

    a_keywords = string_to_keywords(a)
    b_keywords = string_to_keywords(b)

    if not len(a_keywords) or not len(b_keywords):
        return False

    return a_keywords.issubset(b_keywords) or b_keywords.issubset(a_keywords)