from typing import List

from bookaholic._string_utils import compare
from bookaholic._data import Data


FICTION_GENRES = {
    "Action & Adventure": ["action", "adventure"],
    "Comedy": ["comedy", "funny", "humour"],
    "Dystopian": ["dystopia", "dystopian"],
    "Fantasy": ["fantastical", "fantasy", "magic", "magical"],
    "Graphic Novel": ["comic", "comics", "graphic novel", "graphics"],
    "Horror": ["creepy", "horror", "monster", "monsters", "scary", "spooky"],
    "Mystery": ["detective", "mystery", "whodunit"],
    "Sci-Fi": ["science", "scifi"],
    "Thriller": ["roller coaster", "suspense", "suspenseful", "thrill", "thrills", "thriller"]
}
NON_FICTION_GENRES = {
    "Biography": ["autobiographical", "autobiography", "biographical", "biography"],
    "Cooking": ["baking", "cook", "cooking", "food", "kitchen", "home economics"],
    "History": ["historical", "history"],
    "Math": ["algebra", "calculus", "math"],
    "Politics": ["poli sci", "political", "polisci", "politics"],
    "Science": ["biology", "chemistry", "physics", "science"],
    "Self-Help": ["personal development", "personal growth", "self care", "self help", "self improvement"]
} 

class Subject(Data):
    def __init__(self, fiction: bool, genres: List[str]):
        self["fiction"] = fiction
        self["genres"] = genres

    @classmethod
    def new_from_open_library(cls, subjects: List[str]) -> Subject:
        fiction = any((compare(s, "fiction") for s in subjects))
        possible_genres = FICTION_GENRES if fiction else NON_FICTION_GENRES

        genres = []

        for genre, keywords in possible_genres.items():                   

            if any((compare(k, s) for k in keywords for s in subjects)):
                genres.append(genre)

        return Subject(fiction, genres)