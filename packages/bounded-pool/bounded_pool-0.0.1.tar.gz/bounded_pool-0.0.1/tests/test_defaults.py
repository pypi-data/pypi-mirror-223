import asyncio
import time

import pytest

from bounded_pool import (
    BoundedAsyncioPoolExecutor,
    BoundedProcessPoolExecutor,
    BoundedThreadPoolExecutor,
)


@pytest.mark.anyio
async def test_asyncio_defaults():
    async with BoundedAsyncioPoolExecutor() as pool:
        for _ in range(64):
            await pool.submit(asyncio.sleep, 0)


@pytest.mark.parametrize('cls', [BoundedThreadPoolExecutor, BoundedProcessPoolExecutor])
def test_sync_defaults(cls):
    with cls() as pool:
        for _ in range(64):
            pool.submit(time.sleep, 0)
