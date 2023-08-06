import codecs
import string
from typing import List


def read_file(path: str) -> str:
    with codecs.open(path, "r", "utf-8") as f:
        text = f.read()
    return text


def read_word(text: str) -> List[str]:
    for punctation in string.punctuation:
        text = text.replace(punctation, "")
    return text.split()


def exclude_words(words: List[str], excluded_words: List[str]) -> List[str]:
    ex_words = [word.lower() for word in excluded_words]
    return [word for word in words if word.lower() not in ex_words]


def search_line_with_words(text: str, word: str) -> List[int]:
    pass


# def save_to_csv(words: List[Tuple[str, int]], file: str) -> None:
#     #zapisz zmienna words do pliku csv
#     pass
