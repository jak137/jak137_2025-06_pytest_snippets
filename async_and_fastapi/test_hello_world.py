from hello_world import cor_1

import pytest


@pytest.mark.asyncio
async def test_cor_1():
    res = await cor_1()
    assert res == 'Hello world!'
