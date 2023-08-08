import typing as t


from .base import BaseQueueExt


async def transfer_item(
    source: BaseQueueExt,
    destination: BaseQueueExt,
    *,
    cb: t.Callable[[t.Any], None] = None,
) -> None:
    """Atomically transfers an item from one queue to another

    Optionally, a callback routine can be speficied. It will be called after
    the transfer is completed."""

    # ensure that while waiting for place in "b", "a" did not get emptied by
    # another code
    while source.empty() or destination.full():
        await source.return_when_not_empty()
        await destination.return_when_not_full()

    item = source.get_nowait()
    destination.put_nowait(item)

    if cb is not None:
        cb(item)
