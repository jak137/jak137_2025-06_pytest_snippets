import sys
from decimal import Decimal
from io import StringIO
from math import isclose

import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal, assert_series_equal


def test0():
    assert 0.1 + 0.1 == 0.2


@pytest.mark.xfail(reason='Fails due to finite floating point precision.')
def test1():
    assert 0.1 + 0.2 == 0.3


def test2():
    isclose(0.1 + 0.2, 0.3, rel_tol=sys.float_info.epsilon)


planned_costs_csv = '''group,planned_cost_mln
Office,0.3
Services,0.1
'''

planned_costs_mln = pd.read_csv(StringIO(planned_costs_csv))

actual_costs_csv = '''group,item,cost
Office,Electricity,200000
Office,Supplies,100000
Services,Cleaning,110000
'''

costs = pd.read_csv(StringIO(actual_costs_csv))


def test3a():
    df = costs.copy()
    df['cost_mln'] = df['cost'] / 1000_000
    df = df.groupby('group').sum().reset_index()
    df = pd.merge(planned_costs_mln, df, on='group', how='inner')

    df['costs_differ'] = (df['planned_cost_mln'] != df['cost_mln'])
    print('\n\n', df)
    with pytest.raises(AssertionError):
        assert df[df['costs_differ']]['group'].tolist() == ['Services']

    df['costs_differ_2'] = ~pd.Series(
        np.isclose(df['planned_cost_mln'].to_numpy(), df['cost_mln'].to_numpy(),
                   rtol=1.e-12, atol=1.e-12),
        index=df.index
    )
    print('\n\n', df)
    assert df[df['costs_differ_2']]['group'].tolist() == ['Services']


def test4():
    df = costs.copy()
    df['cost'] = df['cost'] * 1.0
    with pytest.raises(AssertionError):
        assert_frame_equal(df, costs)
    assert_frame_equal(df, costs, check_dtype=False)


def test5():
    s1 = pd.Series([1.0, 2.0, 3.0])
    s2 = pd.Series([1.0001, 2.0, 3.0], index=['1st', '2nd', '3rd'])
    with pytest.raises(AssertionError):
        assert_series_equal(s1, s2)
    with pytest.raises(AssertionError):
        assert_series_equal(s1, s2, atol=0.0001)
    assert_series_equal(s1, s2, atol=0.0001, check_index=False)


def test5a():
    np.testing.assert_allclose([1.0, 2.0, 3.0], [1.0001, 2.0, 3.0], atol=0.0001)


def test6():
    assert Decimal('0.1') + Decimal('0.2') == Decimal('0.3')
