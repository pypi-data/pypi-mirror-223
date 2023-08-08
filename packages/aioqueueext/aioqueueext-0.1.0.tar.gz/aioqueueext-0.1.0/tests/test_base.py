import asyncio
import typing as t
import unittest


from aioqueueext.base import BaseQueueExt


class QueueWithDummyPeek(BaseQueueExt):
    peek_result: t.Any

    def _init(self, maxsize) -> None:
        super(BaseQueueExt, self)._init(maxsize)
        super()._init(maxsize)

    def peek_nowait(self) -> t.Any:
        """Some methods rely on peek_nowait which is not implemented in the
        parent class. This is a dummy method for testing the callback
        functionality."""
        return self.peek_result


class TestBaseQueueExt(unittest.IsolatedAsyncioTestCase):
    async def test_on_put_00_setting_callback(self) -> None:
        queue = QueueWithDummyPeek()

        def my_func(_item: t.Any) -> None:
            pass

        self.assertIsNone(queue.on_put_callback)
        queue.set_on_put_callback(my_func)
        self.assertTrue(
            queue._put == queue._put_with_callback,
            "_put must be reassigned to _put_with_callback",
        )
        self.assertIs(
            queue.on_put_callback,
            my_func,
            "set_on_put_callback(my_func) must set the on_put_callback property to my_func",
        )

    async def test_on_put_01_unsetting_callback(self) -> None:
        queue = QueueWithDummyPeek()

        def my_func(_item: t.Any) -> None:
            pass

        __put = queue._put
        queue.set_on_put_callback(my_func)
        queue.set_on_put_callback(None)
        self.assertIsNone(queue.on_put_callback)
        self.assertTrue(
            queue._put != queue._put_with_callback and queue._put == __put,
            "_put must be restored to the original _put",
        )
        self.assertIsNone(
            queue.on_put_callback,
            "set_on_put_callback(None) must set the on_put_callback property to None",
        )

    async def test_on_put_02_calling(self) -> None:
        queue = QueueWithDummyPeek()
        cb_items = []

        def my_func(item: t.Any) -> None:
            cb_items.append(item)

        item1 = object()
        item2 = object()

        queue.set_on_put_callback(my_func)
        await asyncio.sleep(0.2)
        self.assertTrue(
            len(cb_items) == 0, "on_put_callback was called before any put()"
        )

        # put()
        n_calls = len(cb_items)
        await queue.put(item1)
        self.assertEqual(
            len(cb_items), n_calls + 1, "on_put_callback(item) was not called on put()"
        )
        self.assertTrue(
            cb_items[n_calls] is item1,
            "value passed to on_get_callback(item) and put(item) must be the same",
        )

        item1_copy = await queue.get()
        self.assertTrue(
            len(cb_items) == n_calls + 1, "on_put_callback(item) was called on get()"
        )
        self.assertTrue(
            item1_copy is item1, "get() must return the previously enqueued item"
        )

        # put_nowait(), also checks correctness of consequent callback arguments
        n_calls = len(cb_items)
        queue.put_nowait(item2)
        self.assertTrue(
            len(cb_items) == n_calls + 1,
            "on_put_callback(item) was not called on put_nowait()",
        )
        self.assertTrue(
            cb_items[n_calls] is item2,
            "value passed to on_get_callback(item) and put_nowait(item) must be the same",
        )

        item2_copy = queue.get_nowait()
        self.assertTrue(
            len(cb_items) == n_calls + 1,
            "on_put_callback(item) was called on get_nowait()",
        )
        self.assertTrue(
            item2_copy is item2, "get() must return the previously enqueued item"
        )

    async def test_on_get_00_setting_callback(self) -> None:
        queue = QueueWithDummyPeek()

        def my_func(_item: t.Any) -> None:
            pass

        self.assertIsNone(queue.on_get_callback)
        queue.set_on_get_callback(my_func)
        self.assertTrue(
            queue._get == queue._get_with_callback,
            "_get must be reassigned to _get_with_callback",
        )
        self.assertIs(
            queue.on_get_callback,
            my_func,
            "set_on_get_callback(my_func) must set the on_get_callback property to my_func",
        )

    async def test_on_get_01_unsetting_callback(self) -> None:
        queue = QueueWithDummyPeek()

        def my_func(_item: t.Any) -> None:
            pass

        __get = queue._get
        queue.set_on_get_callback(my_func)
        queue.set_on_get_callback(None)
        self.assertIsNone(queue.on_get_callback)
        self.assertTrue(
            queue._get != queue._get_with_callback and queue._get == __get,
            "_get must be restored to the original _get",
        )
        self.assertIsNot(
            queue.on_get_callback,
            my_func,
            "set_on_get_callback(None) must the set the on_get_callback property to None",
        )

    async def test_on_get_02_calling(self) -> None:
        queue = QueueWithDummyPeek()
        cb_items = []

        def my_func(item: t.Any) -> None:
            cb_items.append(item)

        item1 = object()
        item2 = object()

        queue.set_on_get_callback(my_func)
        await asyncio.sleep(0.2)
        self.assertTrue(
            len(cb_items) == 0, "on_get_callback was called before any get()"
        )

        # get()
        n_calls = len(cb_items)
        await queue.put(item1)
        self.assertTrue(
            len(cb_items) == n_calls, "on_get_callback(item) was called on put()"
        )

        queue.peek_result = item1

        n_calls = len(cb_items)
        item1_copy = await queue.get()
        self.assertEqual(
            len(cb_items), n_calls + 1, "on_get_callback(item) was not called on get()"
        )
        self.assertTrue(
            cb_items[n_calls] is item1,
            "on_get_callback(item) call with incorrect arguments",
        )
        self.assertTrue(
            cb_items[n_calls] is item1_copy,
            "value passed to on_get_callback(item) and the one returned by get() must be the same",
        )

        # get_nowait(), also checks correctness of consequent callback arguments
        n_calls = len(cb_items)
        queue.put_nowait(item2)
        self.assertTrue(
            len(cb_items) == n_calls, "on_get_callback(item) was called on put_nowait()"
        )

        queue.peek_result = item2

        n_calls = len(cb_items)
        item2_copy = queue.get_nowait()
        self.assertTrue(
            len(cb_items) == n_calls + 1,
            "on_get_callback(item) was not called on get_nowait()",
        )
        self.assertTrue(
            cb_items[n_calls] is item2,
            "on_get_callback(item) call with incorrect arguments",
        )
        self.assertTrue(
            cb_items[n_calls] is item2_copy,
            "value passed to on_get_callback(item) and the one returned by get_nowait() must be the same",
        )


if __name__ == "__main__":
    unittest.main()
