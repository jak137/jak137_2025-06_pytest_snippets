import sys

import numpy as np
import pyarrow as pa
import pytest

from factorial import factorial1, factorial2
from factorial import NegativeFactorialArgument, NonIntegerFactorialArgument, FactorialArgumentTooLarge


def test_factorial1():
    assert factorial1(1) == 1
    assert factorial1(2) == 2
    assert factorial1(3) == 6


def test_factorial1_at_zero():
    assert factorial1(0) == 1


def test_factorial1_argument_must_be_non_negative():
    with pytest.raises(NegativeFactorialArgument) as ex_info:
        factorial1(-1)
    assert ex_info.value.args == ('Can not compute factorials of -1.',)


def test_factorial1_argument_must_be_integer():
    with pytest.raises(NonIntegerFactorialArgument):
        factorial1(1.1)

    with pytest.raises(NonIntegerFactorialArgument):
        factorial1('three')


def test_factorial1_argument_can_be_numpy_scalar():
    assert factorial1(np.short(3)) == 6


def test_factorial1_argument_can_be_numpy_pyarrow_scalars():
    pa_3 = pa.scalar(3, type=pa.int64())
    assert factorial1(pa_3) == 6
    pa_1_1 = pa.scalar(1.1, type=pa.float32())
    with pytest.raises(NonIntegerFactorialArgument):
        factorial1(pa_1_1)


def test_factorial1_result_can_be_greater_than_max_uint64():
    assert (f21 := factorial1(21)) == 51_090_942_171_709_440_000
    assert f21 > np.iinfo(np.uint64).max
    assert np.iinfo(np.uint64).max == 18_446_744_073_709_551_615


def test_factorial1_handles_recursion_limit():
    with pytest.raises(FactorialArgumentTooLarge):
        assert factorial1(sys.getrecursionlimit())


def test_factorial2():
    assert factorial2(1) == 1
    assert factorial2(2) == 2
    assert factorial2(3) == 6
    assert factorial2(0) == 1

    with pytest.raises(ValueError):
        factorial2(-1)

    with pytest.raises(ValueError):
        factorial2(1.1)

    with pytest.raises(ValueError):
        factorial2('three')

    assert factorial2(np.short(3)) == 6
