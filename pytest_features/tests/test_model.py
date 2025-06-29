from io import StringIO

import numpy as np
import pytest

from sample_module.model import load_texts, texts_to_words, iter_pairs, lengths_counts
from sample_module.model import ToyModel


def test_load_texts():
    payload = '<p>Hello <em>world<em>!</p><p>Ave, munde!</p>'
    assert load_texts(StringIO(payload)) == ['Hello ', 'world', '!', 'Ave, munde!']


@pytest.mark.parametrize("texts,words", [
    ([], []),
    (['Hello'], ['Hello']),
    (['Hello  world'], ['Hello', 'world']),
    (['Hello ', 'world', '!', 'Ave, munde!'], ['Hello', 'world', 'Ave', 'munde'])
])
def test_texts_to_words(texts, words):
    assert texts_to_words(texts) == words


def test_iter_pairs():
    assert list(iter_pairs(['Hello', 'world', 'Ave', 'munde'])) \
           == [('Hello', 'world'), ('world', 'Ave'), ('Ave', 'munde')]


def test_lengths_counts():
    assert dict(lengths_counts(iter([('Hello', 'world'), ('world', 'Ave'), ('Ave', 'munde')]))) == \
           {(5, 5): 1, (5, 3): 1, (3, 5): 1}


def test_toy_model():
    c1 = {(5, 5): 2, (5, 3): 2, (3, 5): 1, (4, 4): 2}
    c2 = {(5, 5): 2, (5, 3): 1, (3, 5): 2, (3, 3): 2}
    toym = ToyModel(c1, c2)
    assert toym.common_counts == [(3, 5), (5, 3), (5, 5)]
    np.testing.assert_equal(toym.y, np.array([1, 2]))
    np.testing.assert_equal(toym.X, np.array([
        [1, 2, 2],
        [2, 1, 2],
    ]))
    ct = {(6, 6): 2, (3, 5): 3, (5, 5): 1}
    p1, p2 = toym.predict(ct)
    assert p2 > p1
