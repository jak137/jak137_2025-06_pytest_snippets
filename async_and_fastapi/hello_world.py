from typing import AsyncGenerator
import asyncio


async def words_source() -> AsyncGenerator[str, None]:
    yield 'Hello'
    await asyncio.sleep(1)
    yield 'world'


async def cor_1() -> str:
    words = [word async for word in words_source()]
    message = ' '.join(words) + '!'
    return message
