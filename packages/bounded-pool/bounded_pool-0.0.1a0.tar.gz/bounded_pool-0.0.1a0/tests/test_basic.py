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
async def test_asyncio_executor_sleeps():
    async with aassert_takes(less=1.5):
        async with BoundedAsyncioPoolExecutor(2) as pool:
            async with aassert_takes(less=0.5):
                for _ in range(2):
                    await pool.submit(asyncio.sleep, 1)

        assert not pool._tasks

    async with aassert_takes(more=3.5):
        async with BoundedAsyncioPoolExecutor(1) as pool:
            async with aassert_takes(more=3):
                for _ in range(4):
                    await pool.submit(asyncio.sleep, 1)

        assert not pool._tasks


@pytest.mark.parametrize('cls', [BoundedThreadPoolExecutor, BoundedProcessPoolExecutor])
def test_sync_executor_sleeps(cls):
    with assert_takes(less=1.5):
        with cls(2) as pool:
            with assert_takes(less=0.5):
                for _ in range(2):
                    pool.submit(time.sleep, 1)

    with assert_takes(more=3.5):
        with cls(1) as pool:
            with assert_takes(more=3):
                for _ in range(2):
                    pool.submit(time.sleep, 1)
