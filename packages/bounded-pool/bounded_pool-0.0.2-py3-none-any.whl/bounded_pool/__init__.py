import multiprocessing
import os
import threading
from abc import ABC
from asyncio import Semaphore, Task, create_task
from concurrent.futures import Executor, ProcessPoolExecutor, ThreadPoolExecutor
from typing import Optional


class BoundedExecutor(ABC):
    def __init__(
        self,
        max_workers: Optional[int] = None,
        max_queue_size: int = 0,
    ):
        self._max_workers = max_workers or self._get_default_max_workers()
        self._max_queue_size = max_queue_size

    @staticmethod
    def _get_default_max_workers() -> int:
        """Return default max workers for current executor."""

    @property
    def _semaphore_size(self):
        return self._max_workers + self._max_queue_size


class BoundedAsyncioPoolExecutor(BoundedExecutor):
    @staticmethod
    def _get_default_max_workers():
        return min(32, (os.cpu_count() or 1) + 4)

    async def __aenter__(self):
        self._semaphore = Semaphore(self._semaphore_size)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        # make sure no tasks being executed
        for _ in range(self._semaphore_size):
            await self._semaphore.acquire()

    async def _acquire(self):
        await self._semaphore.acquire()

    def _release(self, fut):
        self._semaphore.release()

    async def submit(self, coro, *args, **kwargs) -> Task:
        await self._acquire()
        task = create_task(coro(*args, **kwargs))
        task.add_done_callback(self._release)
        return task


class SyncBoundedExecutor(BoundedExecutor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._executor: Optional[Executor] = None
        self._semaphore = None

    def _get_executor(self) -> Executor:
        """Return executor that will actually execute tasks."""

    def _get_semaphore(self):
        """Return semaphore that will actually track tasks queue."""

    def __enter__(self):
        self._executor = self._get_executor()
        self._semaphore = self._get_semaphore()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        assert self._executor
        self._executor.shutdown()

    def _acquire(self):
        assert self._semaphore
        return self._semaphore.acquire()

    def _release(self, fut):
        assert self._semaphore
        return self._semaphore.release()

    def submit(self, fn, *args, **kwargs):
        self._acquire()
        assert self._executor
        future = self._executor.submit(fn, *args, **kwargs)
        future.add_done_callback(self._release)
        return future


class BoundedThreadPoolExecutor(SyncBoundedExecutor):
    @staticmethod
    def _get_default_max_workers():
        return min(32, (os.cpu_count() or 1) + 4)

    def _get_executor(self):
        return ThreadPoolExecutor(self._max_workers)

    def _get_semaphore(self):
        return threading.BoundedSemaphore(self._semaphore_size)


class BoundedProcessPoolExecutor(SyncBoundedExecutor):
    @staticmethod
    def _get_default_max_workers():
        return os.cpu_count() or 1

    def _get_executor(self):
        return ProcessPoolExecutor(self._max_workers)

    def _get_semaphore(self):
        return multiprocessing.BoundedSemaphore(self._semaphore_size)
