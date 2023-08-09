import time
from bounded_pool import BoundedThreadPoolExecutor


def test_example():
    futures = []

    with BoundedThreadPoolExecutor() as pool:
        for _ in range(64):
            future = pool.submit(time.sleep, 1)
            futures.append(future)

    assert futures

    for future in futures:
        assert future.done()
        assert future.result() is None
