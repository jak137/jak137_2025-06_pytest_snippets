import pytest


def test_that_needs_not_sth():
    pass


@pytest.mark.needs_sth
def test_that_needs_sth(sth):
    print(f'\nGot "{sth}"!')
