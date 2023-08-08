"""Provide the AbstractBaseQueueExt"""


import asyncio
import typing as t


class BaseQueueExt(asyncio.Queue):
    """The base class for other asyncio.Queue extension classes in this package

    Implements common methods and initializes some properties.
    """

    _aiopeek_lock: asyncio.Lock
    _aiopeek_item: asyncio.Future
    _aiopeek_decider_func: t.Optional[t.Callable[[t.Any], bool]]

    _on_put_callback: t.Callable[[t.Any], None]
    _on_get_callback: t.Callable[[t.Any], None]

    _empty_event: asyncio.Event
    _not_empty_event: asyncio.Event

    _full_event: asyncio.Event
    _not_full_event: asyncio.Event

    @property
    def on_put_callback(self) -> t.Callable[[t.Any], None]:
        return self._on_put_callback

    @property
    def on_get_callback(self) -> t.Callable[[t.Any], None]:
        return self._on_get_callback

    def _init(self, _maxsize: int) -> None:
        self._aiopeek_lock = asyncio.Lock()
        self._aiopeek_item = None
        self._aiopeek_decider_func = None

        self.__put = self._put
        self.__get = self._get
        self._on_put_callback = None
        self._on_get_callback = None

        self._empty_event = asyncio.Event()
        self._empty_event.set()
        self._not_empty_event = asyncio.Event()

        self._full_event = asyncio.Event()
        self._not_full_event = asyncio.Event()
        self._not_full_event.set()

    def _aiopeek_set_result(self, item) -> None:
        self._aiopeek_item.set_result(item)
        if self._aiopeek_decider_func is None:
            return
        if self._aiopeek_decider_func(item):
            item_copy = self.get_nowait()
            assert item_copy is item

    def _put_with_callback(self, item: t.Any) -> None:
        self.__put(item)
        self._on_put_callback(item)

        if self._aiopeek_lock.locked():
            # a peeker is awaiting
            self._aiopeek_set_result(item)

    def _get_with_callback(self) -> t.Any:
        self._on_get_callback(self.peek_nowait())
        return self.__get()

    async def return_when_empty(self) -> None:
        while not self.empty():
            await self._empty_event.wait()

    async def return_when_not_empty(self) -> None:
        while self.empty():
            await self._not_empty_event.wait()

    async def return_when_not_full(self) -> None:
        while self.full():
            await self._not_full_event.wait()

    async def return_when_full(self) -> None:
        while not self.full():
            await self._full_event.wait()

    async def peek_and_get(self, decider: t.Callable[[t.Any], bool] = None) -> t.Any:
        """async peek_and_get

        When an item becomes available, "decider" is called with the item
        passed to it as a single positional argument. If "decider" returns
        True, the item is popped from the queue before any other async peeker
        or getter can see it.

        When there are multiple async peekers and no getters are awaiting for
        an item, several peekers may see the same item until it is popped by
        one of the peekers.

        Note: If multiple async peekers and getters are awaiting for an item,
        only one of the peekers is guaranteed to see and conditionally get
        (pop) the next item from the queue, unless it gets cancelled before an
        item is available."""

        if not self.empty():
            item = self.peek_nowait()
            if decider is not None:
                if decider(item):
                    item_copy = self.get_nowait()
                    assert item_copy is item
            return item

        async with self._aiopeek_lock:
            self._aiopeek_item = asyncio.Future()
            self._aiopeek_decider_func = decider
            try:
                await self._aiopeek_item
            finally:
                self._aiopeek_item.cancel()
            return self._aiopeek_item.result()

    def peek_nowait(self) -> t.Any:
        raise NotImplementedError

    def set_on_get_callback(self, cb: t.Optional[t.Callable[[t.Any], None]]) -> None:
        """Set a get() and get_nowait() callback function

        The callback function must accept one argument which will contain the
        queued item. Called right before the item is taken out of the queue.
        """
        self._on_get_callback = cb
        if cb is None:
            self._get = self.__get
        else:
            self._get = self._get_with_callback

    def set_on_put_callback(self, cb: t.Optional[t.Callable[[t.Any], None]]) -> None:
        """Set a put() and put_nowait() callback function

        The callback function must accept one argument which will contain the
        queued item. Called right after the item is placed into the queue.
        """
        self._on_put_callback = cb
        if cb is None:
            self._put = self.__put
        else:
            self._put = self._put_with_callback
