"""Provide the QueueExt class"""


import asyncio
import collections
import typing as t


from .base import BaseQueueExt


class QueueExt(BaseQueueExt):
    """A queue with extended features

    In addition to the funtionality provided by asyncio.Queue, it features
    synchronization primitives return_when_empty(), return_when_full(), and
    others. Additionally, it implements the peek_nowait() method that returns
    the next item without removing it from the queue.
    """

    _queue: collections.deque

    def _init(self, _maxsize: int) -> None:
        super()._init(_maxsize)
        self._queue = collections.deque()

    def _put(self, item: t.Any) -> None:
        self._queue.append(item)

        if self._empty_event.is_set():
            self._empty_event.clear()
            self._not_empty_event.set()

        if self.full() and not self._full_event.is_set():
            self._full_event.set()
            self._not_full_event.clear()

    def _get(self) -> t.Any:
        item = self._queue.popleft()

        if len(self._queue) == 0 and not self._empty_event.is_set():
            self._empty_event.set()
            self._not_empty_event.clear()

        if not self.full() and self._full_event.is_set():
            self._full_event.clear()
            self._not_full_event.set()

        return item

    def qsize(self) -> int:
        return len(self._queue)

    def empty(self) -> bool:
        return self.qsize() <= 0

    def full(self) -> bool:
        if self.maxsize <= 0:
            return False
        return self.qsize() >= self.maxsize

    def peek_nowait(self) -> t.Any:
        """Return the item without removing it from the queue"""
        if self.empty():
            raise asyncio.QueueEmpty
        return self._queue[0]
