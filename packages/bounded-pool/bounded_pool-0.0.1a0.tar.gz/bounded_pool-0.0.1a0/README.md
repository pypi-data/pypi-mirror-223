# bounded_pool

[![PyPI version](https://badge.fury.io/py/bounded-pool.svg)](https://badge.fury.io/py/bounded-pool)

Simplistic and universal bounded pool executor that allows to process N tasks
as the same time while limiting size of the queue. Tasks can be functions or
coroutines. Under the hood `bounded_pool` uses threads or processes, depending
on used class. Refer to `tests/test_basic.py` for details.

Tasks will only be submited when there are available workers (specified by
`max_workers`). You can specify `max_queue_size` to allow submiting more
tasks than amount of available workers (so workers won't have to wait for
task creation). Refer to `tests/test_queue.py` for details.

## Example / Showcase

```py
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
```
