import pytest

from bounded_pool import (
    BoundedAsyncioPoolExecutor,
    BoundedProcessPoolExecutor,
    BoundedThreadPoolExecutor,
)


def raiser():
    raise ValueError()


async def araiser():
    raise ValueError()


@pytest.mark.anyio
async def test_asyncio_executor_ignores_exceptions():
    async with BoundedAsyncioPoolExecutor() as pool:
        task = await pool.submit(araiser)

        with pytest.raises(ValueError):
            await task

        task = await pool.submit(araiser)

    with pytest.raises(ValueError):
        await task


@pytest.mark.parametrize('cls', [BoundedThreadPoolExecutor, BoundedProcessPoolExecutor])
def test_sync_executor_ignores_exceptions(cls):
    with cls() as pool:
        task = pool.submit(raiser)

        with pytest.raises(ValueError):
            task.result()

        task = pool.submit(raiser)

    with pytest.raises(ValueError):
        task.result()
