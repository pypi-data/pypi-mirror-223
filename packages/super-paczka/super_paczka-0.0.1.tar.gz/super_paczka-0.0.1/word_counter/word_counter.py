import string
from itertools import groupby
from typing import Tuple, List


def count_words(text: str) -> int:
    pass


def count_specific_words(text: str, word: str) -> Tuple[str, int]:
    pass


def count_word_with_exclusion(text: str, excluded_words: List[str]) -> int:
    pass


def count_all_words(text: str) -> List[Tuple[str, int]]:
    text_wo_punctations = text.translate(str.maketrans("", "", string.punctuation)).split()
    word_tuple = [(w.lower(), 1) for w in text_wo_punctations]
    map_result_sorted = sorted(word_tuple, key=lambda x: x[0])
    reduce_result = []
    for k, g in groupby(map_result_sorted, key=lambda x:x[0]):
        reduce_result.append(_word_reducer(k,g))
    return reduce_result


def _word_reducer(key, values):
    counts = [x[1] for x in values]
    return key, sum(counts)

