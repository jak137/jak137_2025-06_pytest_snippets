from collections import Counter
from functools import reduce
from operator import add
from string import punctuation
from typing import Iterator, Mapping, List, TextIO, Tuple
from html.parser import HTMLParser

import numpy as np
from sklearn.naive_bayes import MultinomialNB

type TextFragment = str
type Word = str


def load_texts(f_in: TextIO) -> List[TextFragment]:
    texts = []

    class TextsCollector(HTMLParser):
        def handle_data(self, data):
            texts.append(data)

    tc = TextsCollector()
    for line in f_in:
        tc.feed(line)
    return texts


def texts_to_words(texts: List[TextFragment]) -> List[Word]:
    trans = str.maketrans('', '', punctuation)
    return reduce(add, ([t.strip() for t in text.translate(trans).split()] for text in texts), [])


def iter_pairs(words: List[Word]) -> Iterator[Tuple[Word, Word]]:
    i1 = iter(words)
    i2 = iter(words)
    next(i2)
    return zip(i1, i2)


type PairOfLenghts = Tuple[int, int]
type PairOfLenghtsCounts = Mapping[PairOfLenghts, int]


def lengths_counts(word_pairs: Iterator[PairOfLenghts]) -> PairOfLenghtsCounts:
    return Counter(map(tuple, (map(len, words_pair) for words_pair in word_pairs)))


class ToyModel:
    def __init__(self, counts1: PairOfLenghtsCounts, counts2: PairOfLenghtsCounts):
        self.common_counts = sorted(set(counts1.keys()) & set(counts2.keys()))
        self.y = np.array([1, 2])
        self.X = np.array([
            [counts1[pair] for pair in self.common_counts],
            [counts2[pair] for pair in self.common_counts],
        ])
        self.clf = MultinomialNB()
        self.clf.fit(self.X, self.y)

    def predict(self, counts: PairOfLenghtsCounts) -> Tuple[float, float]:
        X = [[counts.get(pair, 0) for pair in self.common_counts]]
        p1, p2 = self.clf.predict_proba(X)[0]
        return p1, p2
