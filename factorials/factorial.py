import numbers

import pyarrow as pa


class NegativeFactorialArgument(ValueError):
    """Raised when factorials function is called with negative argument."""


class NonIntegerFactorialArgument(ValueError):
    """Raised when factorials function is called with non-integer argument."""


class FactorialArgumentTooLarge(ValueError):
    """Raised when factorials function is called with too large argument for which the algorithm fails."""


def factorial1(n: numbers.Integral | pa.lib.Scalar) -> int:
    if isinstance(n, pa.lib.Scalar):
        n = n.as_py()
    if not isinstance(n, numbers.Integral):
        raise NonIntegerFactorialArgument(f'Only factorials of integers can be computed. '
                                          f'Received: {repr(n)} of type {type(n)}.')
    if n < 0:
        raise NegativeFactorialArgument(f'Can not compute factorials of {n}.')
    elif n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        try:
            return n * factorial1(n - 1)
        except RecursionError:
            raise FactorialArgumentTooLarge


from typing import Annotated
from pydantic import Field, TypeAdapter

PositiveInteger = Annotated[int, Field(gt=-1)]


def factorial2(n: PositiveInteger):
    n = TypeAdapter(PositiveInteger).validate_python(n)
    if n in {0, 1}:
        return 1
    else:
        return n * factorial2(n - 1)
