"""Provide the OneQueueExt class"""


import asyncio
import typing as t


from .base import BaseQueueExt


class OneQueueExt(BaseQueueExt):
    """A single-slot queue with extended features

    In addition to the funtionality provided by asyncio.Queue, it features
    synchronization primitives return_when_empty(), return_when_full(), and
    others. Additionally, it implements the peek_nowait() method that returns
    the item without removing it from the queue.
    """

    _item: t.Any

    def __init__(self) -> None:
        super().__init__(maxsize=1)

    def _init(self, _maxsize: int) -> None:
        super()._init(_maxsize)
        self._item = None

    def _put(self, item: t.Any) -> None:
        self._empty_event.clear()
        self._not_empty_event.set()

        self._full_event.set()
        self._not_full_event.clear()

        self._item = item

    def _get(self) -> t.Any:
        self._empty_event.set()
        self._not_empty_event.clear()

        self._full_event.clear()
        self._not_full_event.set()

        return self._item

    def qsize(self) -> int:
        if self._empty_event.is_set():
            return 0
        return 1

    def empty(self) -> bool:
        return self.qsize() <= 0

    def full(self) -> bool:
        return self.qsize() > 0

    def peek_nowait(self) -> t.Any:
        """Return the queued item without removing it from the queue"""
        if self.empty():
            raise asyncio.QueueEmpty
        return self._item
