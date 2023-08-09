import asyncio

import pytest
import time

from bounded_pool import (
    BoundedAsyncioPoolExecutor,
    BoundedProcessPoolExecutor,
    BoundedThreadPoolExecutor,
)

from .conftest import aassert_takes, assert_takes


@pytest.mark.anyio
async def test_asyncio_executor_queues():
    async with BoundedAsyncioPoolExecutor(1, 1) as pool:
        async with aassert_takes(more=1, less=2):
            async with aassert_takes(less=0.5):
                await pool.submit(asyncio.sleep, 1)
                await pool.submit(asyncio.sleep, 1)
            await pool.submit(asyncio.sleep, 1)


@pytest.mark.parametrize('cls', [BoundedThreadPoolExecutor, BoundedProcessPoolExecutor])
def test_sync_executor_queues(cls):
    with cls(1, 1) as pool:
        with assert_takes(more=1, less=2):
            with assert_takes(less=0.5):
                pool.submit(time.sleep, 1)
                pool.submit(time.sleep, 1)
            pool.submit(time.sleep, 1)
