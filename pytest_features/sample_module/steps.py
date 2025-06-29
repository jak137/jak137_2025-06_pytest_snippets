from typing import TextIO, Tuple

from .model import load_texts, texts_to_words, iter_pairs, lengths_counts
from .model import ToyModel


def build_model(f1_in: TextIO, f2_in: TextIO) -> ToyModel:
    c1 = lengths_counts(iter_pairs(texts_to_words(load_texts(f1_in))))
    c2 = lengths_counts(iter_pairs(texts_to_words(load_texts(f2_in))))
    return ToyModel(c1, c2)


def predict_text(model: ToyModel, text: str) -> Tuple[float, float]:
    ct = lengths_counts(iter_pairs(texts_to_words([text])))
    return model.predict(ct)
